# Changelog

### [1.4.1](https://www.github.com/readthedocs-fr/bin-server/compare/v1.4.0...v1.4.1) (2026-02-03)


### Bug Fixes

* cgi has been removed from the python stdlib ([0a68559](https://www.github.com/readthedocs-fr/bin-server/commit/0a6855960bf1439b398d1ad14cf60c493b9250d8))

## [1.4.0](https://www.github.com/readthedocs-fr/bin-server/compare/v1.3.0...v1.4.0) (2023-03-13)


### Features

* **config:** support redis password and username ([26b4fa4](https://www.github.com/readthedocs-fr/bin-server/commit/26b4fa4a67ff99fee9b0dd1f451017b32addb911))
* **front:** add option to easily change lang ([f829940](https://www.github.com/readthedocs-fr/bin-server/commit/f8299401c65f8d14cf8e9bddde93246926d5859d))
* **front:** externalize SVGs ([fbdf918](https://www.github.com/readthedocs-fr/bin-server/commit/fbdf918b24a693324619c75d656387709a016472))
* **highlight:** allow all languages ([9f39fef](https://www.github.com/readthedocs-fr/bin-server/commit/9f39fef7feeb621cfa98c2a2e1e08f04a529dd55)), closes [#119](https://www.github.com/readthedocs-fr/bin-server/issues/119)
* **rtdbin.sh:** configurable destination site ([25f21e9](https://www.github.com/readthedocs-fr/bin-server/commit/25f21e93c436011778cc13b0e689ebf70ec3b4a5))
* **tests:** new FakeConfig utility ([c83c36f](https://www.github.com/readthedocs-fr/bin-server/commit/c83c36faf4da4d3404984d5ba1def1c3d5892cf1))
* **tests:** test the /new url ([9e71701](https://www.github.com/readthedocs-fr/bin-server/commit/9e71701bd55be184b733279254798cd835c21149))


### Bug Fixes

* **front:** typos in form placeholder tutorial ([2adcc2f](https://www.github.com/readthedocs-fr/bin-server/commit/2adcc2f9198f54dccaadaaeb21499dcb22f4230c)), closes [#168](https://www.github.com/readthedocs-fr/bin-server/issues/168)
* **tests:** use cleanup instead of tearDown ([c3d27fb](https://www.github.com/readthedocs-fr/bin-server/commit/c3d27fbcd415fb898ac47ecc47e1af8b8584b1f9))

## [1.3.0](https://www.github.com/readthedocs-fr/bin-server/compare/v1.2.0...v1.3.0) (2021-11-19)


### Features

* remove frontend for bin deletion ([595e8e5](https://www.github.com/readthedocs-fr/bin-server/commit/595e8e5831be969eeb7aeaf338aba69004f85f92))


### Bug Fixes

* force identifier length to IDENTSIZE ([9c8865e](https://www.github.com/readthedocs-fr/bin-server/commit/9c8865e3fc2d2eecfe45e956ae4648adceafe0e0))
* include assets' root files ([f0bdd82](https://www.github.com/readthedocs-fr/bin-server/commit/f0bdd825ba6f90414ea133ebd15a07a9447f9995))
* undeclared 'token' error ([1c4e5e3](https://www.github.com/readthedocs-fr/bin-server/commit/1c4e5e3c0171a868e067d6136bdc0e26b369f2a9))


### Dependencies

* update pygments and other dependencies ([b8b6eee](https://www.github.com/readthedocs-fr/bin-server/commit/b8b6eee7cba2b33faf232da4c6d000822184d669))

## [1.2.0](https://www.github.com/readthedocs-fr/bin-server/compare/v1.1.2...v1.2.0) (2021-04-22)


### Features

* bin deletion ([7e45897](https://www.github.com/readthedocs-fr/bin-server/commit/7e45897ef00b4130a210cca818545647a4a56a01))
* favicon ([5754e8c](https://www.github.com/readthedocs-fr/bin-server/commit/5754e8cff804d91a24f869f51f23505486e8189a))

### [1.1.2](https://www.github.com/readthedocs-fr/bin-server/compare/v1.1.1...v1.1.2) (2021-04-18)


### Bug Fixes

* **highlight:** optional startinline ([0bc3f7b](https://www.github.com/readthedocs-fr/bin-server/commit/0bc3f7b05a65490a962f830b1947f40397f14b84))

### [1.1.1](https://www.github.com/readthedocs-fr/bin-server/compare/v1.1.0...v1.1.1) (2021-04-12)


### Bug Fixes

* **manifest:** update version file path ([c709527](https://www.github.com/readthedocs-fr/bin-server/commit/c709527a4d7715d83b01a2c9c977d5edf892d48a)), closes [#132](https://www.github.com/readthedocs-fr/bin-server/issues/132)

## [1.1.0](https://www.github.com/readthedocs-fr/bin-server/compare/v1.0.2...v1.1.0) (2021-04-11)


### Features

* introduce logging ([d256237](https://www.github.com/readthedocs-fr/bin-server/commit/d256237a5c7f01f14c34bb992474f719d4818c34))
* new /report endpoint to report a snippet ([70c7ab8](https://www.github.com/readthedocs-fr/bin-server/commit/70c7ab87af3d148e9dc3773d118f4356eb0dd572)), closes [#110](https://www.github.com/readthedocs-fr/bin-server/issues/110)


### Bug Fixes

* identify form using name ([da6ce4e](https://www.github.com/readthedocs-fr/bin-server/commit/da6ce4e0b5b07b0bc932ee60b3ac35ff7313d293))
* lang and extension parsing ([dd84f12](https://www.github.com/readthedocs-fr/bin-server/commit/dd84f12177ed240006f919a4a6a777b3ca187eaa))
* synchronize /req.txt and /docs/req.txt ([8172198](https://www.github.com/readthedocs-fr/bin-server/commit/81721988a3bff6bfc2913fac327e5ad58f427503))

### [1.0.2](https://www.github.com/readthedocs-fr/bin-server/compare/v1.0.1...v1.0.2) (2021-03-29)


### Bug Fixes

* lang and extension parsing ([5868f01](https://www.github.com/readthedocs-fr/bin-server/commit/5868f01d632e4309bfb9b4dc61b3003b4fdce5b0))
* prevent generated id to override with routes ([466c111](https://www.github.com/readthedocs-fr/bin-server/commit/466c11154201c6d337c8de730c4b4705eea78a59))
* **release-please:** workflow errors ([#125](https://www.github.com/readthedocs-fr/bin-server/issues/125)) ([16afd6b](https://www.github.com/readthedocs-fr/bin-server/commit/16afd6b57d76c594b680f04c377979cbaa9f78b2))
* snippet duplication typo ([ebb6443](https://www.github.com/readthedocs-fr/bin-server/commit/ebb6443908b29daaa1ba6a108c968b5d02778940))
