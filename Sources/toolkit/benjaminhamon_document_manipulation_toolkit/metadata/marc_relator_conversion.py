# See https://www.loc.gov/marc/relators/relacode.html


def convert_term_to_code(role_term: str) -> str: # pylint: disable = too-many-return-statements, too-many-branches, too-many-statements
    role_term = role_term.lower()

# cspell:disable
    if role_term == "abridger":
        return "abr"
    if role_term == "art copyist":
        return "acp"
    if role_term == "actor":
        return "act"
    if role_term == "art director":
        return "adi"
    if role_term == "adapter":
        return "adp"
    if role_term == "author of afterword, colophon, etc.":
        return "aft"
    if role_term == "announcer":
        return "anc"
    if role_term == "analyst":
        return "anl"
    if role_term == "animator":
        return "anm"
    if role_term == "annotator":
        return "ann"
    if role_term == "bibliographic antecedent":
        return "ant"
    if role_term == "appellee":
        return "ape"
    if role_term == "appellant":
        return "apl"
    if role_term == "applicant":
        return "app"
    if role_term == "author in quotations or text abstracts":
        return "aqt"
    if role_term == "architect":
        return "arc"
    if role_term == "artistic director":
        return "ard"
    if role_term == "arranger":
        return "arr"
    if role_term == "artist":
        return "art"
    if role_term == "assignee":
        return "asg"
    if role_term == "associated name":
        return "asn"
    if role_term == "autographer":
        return "ato"
    if role_term == "attributed name":
        return "att"
    if role_term == "auctioneer":
        return "auc"
    if role_term == "author of dialog":
        return "aud"
    if role_term == "audio engineer":
        return "aue"
    if role_term == "author of introduction, etc.":
        return "aui"
    if role_term == "audio producer":
        return "aup"
    if role_term == "screenwriter":
        return "aus"
    if role_term == "author":
        return "aut"
    if role_term == "binding designer":
        return "bdd"
    if role_term == "bookjacket designer":
        return "bjd"
    if role_term == "book artist":
        return "bka"
    if role_term == "book designer":
        return "bkd"
    if role_term == "book producer":
        return "bkp"
    if role_term == "blurb writer":
        return "blw"
    if role_term == "binder":
        return "bnd"
    if role_term == "bookplate designer":
        return "bpd"
    if role_term == "broadcaster":
        return "brd"
    if role_term == "braille embosser":
        return "brl"
    if role_term == "bookseller":
        return "bsl"
    if role_term == "casting director":
        return "cad"
    if role_term == "caster":
        return "cas"
    if role_term == "conceptor":
        return "ccp"
    if role_term == "choreographer":
        return "chr"
    if role_term == "collaborator":
        return "clb"
    if role_term == "client":
        return "cli"
    if role_term == "calligrapher":
        return "cll"
    if role_term == "colorist":
        return "clr"
    if role_term == "collotyper":
        return "clt"
    if role_term == "commentator":
        return "cmm"
    if role_term == "composer":
        return "cmp"
    if role_term == "compositor":
        return "cmt"
    if role_term == "conductor":
        return "cnd"
    if role_term == "cinematographer":
        return "cng"
    if role_term == "censor":
        return "cns"
    if role_term == "contestant-appellee":
        return "coe"
    if role_term == "collector":
        return "col"
    if role_term == "compiler":
        return "com"
    if role_term == "conservator":
        return "con"
    if role_term == "camera operator":
        return "cop"
    if role_term == "collection registrar":
        return "cor"
    if role_term == "contestant":
        return "cos"
    if role_term == "contestant-appellant":
        return "cot"
    if role_term == "court governed":
        return "cou"
    if role_term == "cover designer":
        return "cov"
    if role_term == "copyright claimant":
        return "cpc"
    if role_term == "complainant-appellee":
        return "cpe"
    if role_term == "copyright holder":
        return "cph"
    if role_term == "complainant":
        return "cpl"
    if role_term == "complainant-appellant":
        return "cpt"
    if role_term == "creator":
        return "cre"
    if role_term == "correspondent":
        return "crp"
    if role_term == "corrector":
        return "crr"
    if role_term == "court reporter":
        return "crt"
    if role_term == "consultant":
        return "csl"
    if role_term == "consultant to a project":
        return "csp"
    if role_term == "costume designer":
        return "cst"
    if role_term == "contributor":
        return "ctb"
    if role_term == "contestee-appellee":
        return "cte"
    if role_term == "cartographer":
        return "ctg"
    if role_term == "contractor":
        return "ctr"
    if role_term == "contestee":
        return "cts"
    if role_term == "contestee-appellant":
        return "ctt"
    if role_term == "curator":
        return "cur"
    if role_term == "commentator for written text":
        return "cwt"
    if role_term == "dubbing director":
        return "dbd"
    if role_term == "distribution place":
        return "dbp"
    if role_term == "defendant":
        return "dfd"
    if role_term == "defendant-appellee":
        return "dfe"
    if role_term == "defendant-appellant":
        return "dft"
    if role_term == "degree committee member":
        return "dgc"
    if role_term == "degree granting institution":
        return "dgg"
    if role_term == "degree supervisor":
        return "dgs"
    if role_term == "dissertant":
        return "dis"
    if role_term == "dj":
        return "djo"
    if role_term == "delineator":
        return "dln"
    if role_term == "dancer":
        return "dnc"
    if role_term == "donor":
        return "dnr"
    if role_term == "depicted":
        return "dpc"
    if role_term == "depositor":
        return "dpt"
    if role_term == "draftsman":
        return "drm"
    if role_term == "director":
        return "drt"
    if role_term == "designer":
        return "dsr"
    if role_term == "distributor":
        return "dst"
    if role_term == "data contributor":
        return "dtc"
    if role_term == "dedicatee":
        return "dte"
    if role_term == "data manager":
        return "dtm"
    if role_term == "dedicator":
        return "dto"
    if role_term == "dubious author":
        return "dub"
    if role_term == "editor of compilation":
        return "edc"
    if role_term == "editorial director":
        return "edd"
    if role_term == "editor of moving image work":
        return "edm"
    if role_term == "editor":
        return "edt"
    if role_term == "engraver":
        return "egr"
    if role_term == "electrician":
        return "elg"
    if role_term == "electrotyper":
        return "elt"
    if role_term == "engineer":
        return "eng"
    if role_term == "enacting jurisdiction":
        return "enj"
    if role_term == "etcher":
        return "etr"
    if role_term == "event place":
        return "evp"
    if role_term == "expert":
        return "exp"
    if role_term == "facsimilist":
        return "fac"
    if role_term == "film distributor":
        return "fds"
    if role_term == "field director":
        return "fld"
    if role_term == "film editor":
        return "flm"
    if role_term == "film director":
        return "fmd"
    if role_term == "filmmaker":
        return "fmk"
    if role_term == "former owner":
        return "fmo"
    if role_term == "film producer":
        return "fmp"
    if role_term == "funder":
        return "fnd"
    if role_term == "founder":
        return "fon"
    if role_term == "first party":
        return "fpy"
    if role_term == "forger":
        return "frg"
    if role_term == "game developer":
        return "gdv"
    if role_term == "geographic information specialist":
        return "gis"
    if role_term == "t 	graphic technician":
        return "-gr"
    if role_term == "host institution":
        return "his"
    if role_term == "honoree":
        return "hnr"
    if role_term == "host":
        return "hst"
    if role_term == "illustrator":
        return "ill"
    if role_term == "illuminator":
        return "ilu"
    if role_term == "inscriber":
        return "ins"
    if role_term == "inventor":
        return "inv"
    if role_term == "issuing body":
        return "isb"
    if role_term == "instrumentalist":
        return "itr"
    if role_term == "interviewee":
        return "ive"
    if role_term == "interviewer":
        return "ivr"
    if role_term == "judge":
        return "jud"
    if role_term == "jurisdiction governed":
        return "jug"
    if role_term == "laboratory":
        return "lbr"
    if role_term == "librettist":
        return "lbt"
    if role_term == "laboratory director":
        return "ldr"
    if role_term == "lead":
        return "led"
    if role_term == "libelee-appellee":
        return "lee"
    if role_term == "libelee":
        return "lel"
    if role_term == "lender":
        return "len"
    if role_term == "libelee-appellant":
        return "let"
    if role_term == "lighting designer":
        return "lgd"
    if role_term == "libelant-appellee":
        return "lie"
    if role_term == "libelant":
        return "lil"
    if role_term == "libelant-appellant":
        return "lit"
    if role_term == "landscape architect":
        return "lsa"
    if role_term == "licensee":
        return "lse"
    if role_term == "licensor":
        return "lso"
    if role_term == "lithographer":
        return "ltg"
    if role_term == "lyricist":
        return "lyr"
    if role_term == "music copyist":
        return "mcp"
    if role_term == "metadata contact":
        return "mdc"
    if role_term == "medium":
        return "med"
    if role_term == "manufacture place":
        return "mfp"
    if role_term == "manufacturer":
        return "mfr"
    if role_term == "makeup artist":
        return "mka"
    if role_term == "moderator":
        return "mod"
    if role_term == "monitor":
        return "mon"
    if role_term == "marbler":
        return "mrb"
    if role_term == "markup editor":
        return "mrk"
    if role_term == "musical director":
        return "msd"
    if role_term == "metal-engraver":
        return "mte"
    if role_term == "minute taker":
        return "mtk"
    if role_term == "music programmer":
        return "mup"
    if role_term == "musician":
        return "mus"
    if role_term == "mixing engineer":
        return "mxe"
    if role_term == "news anchor":
        return "nan"
    if role_term == "narrator":
        return "nrt"
    if role_term == "onscreen participant":
        return "onp"
    if role_term == "opponent":
        return "opn"
    if role_term == "originator":
        return "org"
    if role_term == "organizer":
        return "orm"
    if role_term == "onscreen presenter":
        return "osp"
    if role_term == "other":
        return "oth"
    if role_term == "owner":
        return "own"
    if role_term == "place of address":
        return "pad"
    if role_term == "panelist":
        return "pan"
    if role_term == "patron":
        return "pat"
    if role_term == "publishing director":
        return "pbd"
    if role_term == "publisher":
        return "pbl"
    if role_term == "project director":
        return "pdr"
    if role_term == "proofreader":
        return "pfr"
    if role_term == "photographer":
        return "pht"
    if role_term == "platemaker":
        return "plt"
    if role_term == "permitting agency":
        return "pma"
    if role_term == "production manager":
        return "pmn"
    if role_term == "printer of plates":
        return "pop"
    if role_term == "papermaker":
        return "ppm"
    if role_term == "puppeteer":
        return "ppt"
    if role_term == "praeses":
        return "pra"
    if role_term == "process contact":
        return "prc"
    if role_term == "production personnel":
        return "prd"
    if role_term == "presenter":
        return "pre"
    if role_term == "performer":
        return "prf"
    if role_term == "programmer":
        return "prg"
    if role_term == "printmaker":
        return "prm"
    if role_term == "production company":
        return "prn"
    if role_term == "producer":
        return "pro"
    if role_term == "production place":
        return "prp"
    if role_term == "production designer":
        return "prs"
    if role_term == "printer":
        return "prt"
    if role_term == "provider":
        return "prv"
    if role_term == "patent applicant":
        return "pta"
    if role_term == "plaintiff-appellee":
        return "pte"
    if role_term == "plaintiff":
        return "ptf"
    if role_term == "patent holder":
        return "pth"
    if role_term == "plaintiff-appellant":
        return "ptt"
    if role_term == "publication place":
        return "pup"
    if role_term == "rapporteur":
        return "rap"
    if role_term == "rubricator":
        return "rbr"
    if role_term == "recordist":
        return "rcd"
    if role_term == "recording engineer":
        return "rce"
    if role_term == "addressee":
        return "rcp"
    if role_term == "radio director":
        return "rdd"
    if role_term == "redaktor":
        return "red"
    if role_term == "renderer":
        return "ren"
    if role_term == "researcher":
        return "res"
    if role_term == "reviewer":
        return "rev"
    if role_term == "radio producer":
        return "rpc"
    if role_term == "repository":
        return "rps"
    if role_term == "reporter":
        return "rpt"
    if role_term == "responsible party":
        return "rpy"
    if role_term == "respondent-appellee":
        return "rse"
    if role_term == "restager":
        return "rsg"
    if role_term == "respondent":
        return "rsp"
    if role_term == "restorationist":
        return "rsr"
    if role_term == "respondent-appellant":
        return "rst"
    if role_term == "research team head":
        return "rth"
    if role_term == "research team member":
        return "rtm"
    if role_term == "remix artist":
        return "rxa"
    if role_term == "scientific advisor":
        return "sad"
    if role_term == "scenarist":
        return "sce"
    if role_term == "sculptor":
        return "scl"
    if role_term == "scribe":
        return "scr"
    if role_term == "sound engineer":
        return "sde"
    if role_term == "sound designer":
        return "sds"
    if role_term == "secretary":
        return "sec"
    if role_term == "special effects provider":
        return "sfx"
    if role_term == "stage director":
        return "sgd"
    if role_term == "signer":
        return "sgn"
    if role_term == "supporting host":
        return "sht"
    if role_term == "seller":
        return "sll"
    if role_term == "singer":
        return "sng"
    if role_term == "speaker":
        return "spk"
    if role_term == "sponsor":
        return "spn"
    if role_term == "second party":
        return "spy"
    if role_term == "surveyor":
        return "srv"
    if role_term == "set designer":
        return "std"
    if role_term == "setting":
        return "stg"
    if role_term == "storyteller":
        return "stl"
    if role_term == "stage manager":
        return "stm"
    if role_term == "standards body":
        return "stn"
    if role_term == "stereotyper":
        return "str"
    if role_term == "software developer":
        return "swd"
    if role_term == "television writer":
        return "tau"
    if role_term == "technical director":
        return "tcd"
    if role_term == "teacher":
        return "tch"
    if role_term == "thesis advisor":
        return "ths"
    if role_term == "television director":
        return "tld"
    if role_term == "television guest":
        return "tlg"
    if role_term == "television host":
        return "tlh"
    if role_term == "television producer":
        return "tlp"
    if role_term == "transcriber":
        return "trc"
    if role_term == "translator":
        return "trl"
    if role_term == "type designer":
        return "tyd"
    if role_term == "typographer":
        return "tyg"
    if role_term == "university place":
        return "uvp"
    if role_term == "voice actor":
        return "vac"
    if role_term == "videographer":
        return "vdg"
    if role_term == "visual effects provider":
        return "vfx"
    if role_term == "vocalist":
        return "voc"
    if role_term == "writer of added commentary":
        return "wac"
    if role_term == "writer of added lyrics":
        return "wal"
    if role_term == "writer of accompanying material":
        return "wam"
    if role_term == "writer of added text":
        return "wat"
    if role_term == "woodcutter":
        return "wdc"
    if role_term == "wood engraver":
        return "wde"
    if role_term == "writer of introduction":
        return "win"
    if role_term == "witness":
        return "wit"
    if role_term == "writer of preface":
        return "wpr"
    if role_term == "writer of supplementary textual content":
        return "wst"
# cspell:enable

    raise ValueError("Unknown role term: '%s'" % role_term)
