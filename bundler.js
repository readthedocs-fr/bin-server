import { readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { join, extname, basename, dirname, isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';
import { gzipSync } from 'node:zlib';
import glob from 'fast-glob';
// https://github.com/mrmlnc/fast-glob#pattern-syntax
import slash from 'slash';
import cssnano from 'cssnano';
import postcss from 'postcss';
import { minify as minifyJs } from 'terser';
import { optimize as minifySvg } from 'svgo';
import { fileURLToPath } from 'node:url';

const JS_REG = /<script.*src="([\w/.-]+)"/gi;
const CSS_REG = /<link.*(?:rel="?stylesheet"?.*href="([\w/.-]+)"|href="([\w/.-]+)".*rel="?stylesheet"?)/gi;
const SVG_REG = /<img.*src="([\w/.-]+\.svg)"/gi;

class Processor {
  /**
   * Creates a new processor.
   * @param {RegExp} pattern The RegExp pattern to match the resources path for this processor.
   * @param {(file: string, path: string) => Promise<string> | string} processor The processor function.
   */
  constructor(pattern, processor) {
    this.pattern = pattern;
    this.processor = processor;
  }

  /**
   * Get the paths to the resources that this processor can process from the given HTML file.
   * @param {HTMLFile} html The HTML file.
   * @returns {Generator<unknown, undefined, string>} The paths to the resources that this processor can process.
   */
  *getPaths(html) {
    for (const matches of html.content.matchAll(this.pattern))
      yield matches[1] || matches[2];
  }

  /**
   * Process (minify) the given resource file.
   * @param {string} path The path to the resource file.
   * @returns {Promise<string>} The processed (minified) file content.
   */
  async process(path) {
    return this.processor(readFileSync(path, 'utf8'), path);
  }
}

class HTMLFile {
  /**
   * Creates a new HTML file handle.
   * @param {string} path The path to the HTML file. 
   */
  constructor(path) {
    this.path = path;
    this.content = readFileSync(path, 'utf8');
    this.changed = false;
  }

  /**
   * Creates a new resource linked to this HTML file.
   * @param {string} content The processed content of the resource.
   * @param {string} path The file system path to the resource.
   * @returns {Resource} A Resource instance.
   */
  newResource(content, path, pathInHtml) {
    return new Resource(content, path, this);
  }
}

class Resource {
  constructor(content, path,  htmlFile) {
    this.path = path;
    this.content = content;
    this.hash = createHash('md5').update(content).digest('hex').slice(0, 20);
    this.htmls = [htmlFile];
  }
}

if (process.argv.length < 4) {
  console.error(`Usage: bin-bundler <htmlGlob> <assetDirectory> (gzipLevel)`);
  process.exit(1);
}

let [,, htmlGlob, assetDirectory] = process.argv;
const gzipLevel = process.argv[4] && parseInt(process.argv[4], 10);

const projectRoot = fileURLToPath(new URL('.', import.meta.url));

if (!isAbsolute(assetDirectory)) {
  assetDirectory = join(projectRoot, assetDirectory);
}

const htmlPaths = await glob(slash(htmlGlob), { onlyFiles: true, cwd: projectRoot });
if (htmlPaths.length === 0)
  throw new Error('Found 0 HTML file.');

const cssMinifier = postcss([cssnano({ preset: 'advanced' })]);

// A map of supported processors.
const processors = {
  __proto__: null,
  js: new Processor(JS_REG, (file, path) =>
    minifyJs({ [path]: file }, { sourceMap: false }).then(({ code }) => code)),
  css: new Processor(CSS_REG, (file, from) =>
    cssMinifier.process(file, { map: false, from }).then(({ css }) => css)),
  svg: new Processor(SVG_REG, (file) => minifySvg(file).data),
};

// An array of HTML file handle.
const htmlFiles = [];

// This contains all processed resources, contained in processor kind.
const changes = Object.create(null);
for (const kind in processors) {
  changes[kind] = new Map();
}

// The HTML relative asset path.
const assetPath = '/' + basename(assetDirectory);

// For each html file, and kind of resource, process (and gzip) resources
for (const htmlPath of htmlPaths) {
  if (!htmlPath.endsWith('.html')) continue;

  const htmlFile = new HTMLFile(htmlPath);
  htmlFiles.push(htmlFile);

  for (const kind in changes) {
    const processor = processors[kind];
    const target = changes[kind];

    // The resource path in the HTML file.
    for (const resourcePath of processor.getPaths(htmlFile)) {
      // If the resource has already been processed,
      // push this html file so that it is also updated.
      //
      // Else process the resource and add it to the changes map.
      // 
      if (target.has(resourcePath)) {
        target.get(resourcePath).htmls.push(htmlFile);
      } else {
        // The real resource path in the current file system.
        const realPath = join(assetDirectory, resourcePath.startsWith(assetPath) ?
                                                resourcePath.slice(assetPath.length) :
                                                resourcePath);

        try {
          let content = await processor.process(realPath);

          if (gzipLevel)
            content = gzipSync(content, { level: gzipLevel });

          target.set(resourcePath, htmlFile.newResource(content, realPath, resourcePath));
        } catch (error) {
          console.error('At %s for %s files: %s:',
                        htmlPath,
                        kind.toUpperCase(),
                        resourcePath);
          throw error;
        }
      }
    }
  }
}

// Save all changed resources files.
for (const kind in changes) {
  for (const [pathInHtml, resource] of changes[kind].entries()) {
    const suffix = resource.hash +
                   `${extname(resource.path)}${gzipLevel ? '.gz' : ''}`;
    const dest = join(dirname(resource.path), suffix);

    unlinkSync(resource.path);
    writeFileSync(dest, resource.content);

    const newPath = slash(join(dirname(pathInHtml), suffix));
    for (const html of resource.htmls) {
      html.content = html.content.replaceAll(pathInHtml, newPath);
      html.changed = true;
    }
  }
}

// Edit and save all changed HTML files.
for (const html of htmlFiles)
  if (html.changed)
    writeFileSync(html.path, html.content);

console.log('Successfully bundled bin assets.');
