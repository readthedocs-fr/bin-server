import textwrap
import itertools
from genpw import pronounceable_passwd

fake_database = {
    "abc": textwrap.dedent("""\
        void _delete_from_node(Tree tree, Duck duck) {
            generic_type _duck = getMemberByName(tree, duck);
            if(strcmp(duck->name, tree->root->current->name) == 0) {
                free(tree);
            }
            delete_tree_from_node(_duck); 
        }
        """)
}

class Snippet:
    def __init__(self, ident, code):
        self.id = ident
        self.code = code

    @classmethod
    def create(cls, code):
        ident = pronounceable_passwd(6)
        fake_database[ident] = code
        return cls(ident, code)

    @classmethod
    def get_by_id(cls, snippet_id):
        code = fake_database[snippet_id]
        return cls(snippet_id, code)
