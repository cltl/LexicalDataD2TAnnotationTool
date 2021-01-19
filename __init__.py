
from .lexicon_utils import create_lexicon_data_annotation_tool

from .lexicon_utils import add_frame_to_info

from .lexicon_utils import add_lu_to_info

from .lexicon_utils import add_lemma_to_pos_to_lu_urls

from .typicality_utils import initialize_typical_frames

from .typicality_utils import update_typical_frames

from .typicality_utils import create_lexical_lookup_per_eventtype

from .lexicon_utils import lemmas_from_lu_name

## loading
import os
from .rdf_utils import load_nt_graph
dir_path = os.path.dirname(os.path.realpath(__file__))

premon_nt = os.path.join(dir_path, 'res/premon/premon-2018a-fn17-noinf.nt')
if os.path.exists(premon_nt):
    premon = load_nt_graph(nt_path=premon_nt)
else:
    print('please run bash install.sh')




