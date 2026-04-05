from pathlib import Path
from typing import Literal, Dict, List, TypedDict, Any, Union, Callable, Optional
from .Project import Project, Target, Block
from .translator import WrappedTranslator

Number = Union[int, float]

class VariableDict(TypedDict):
    name: str
    default: Any
    real_name: str
    type: Literal["v", "l"]

class CostumeDict(TypedDict):
    path: str
    rotationCenterX: Number
    rotationCenterY: Number

class AssetsDict(TypedDict):
    sounds: Dict[str, str] # key: name, value: basename
    costumes: Dict[str, CostumeDict] # key: name, value: {path: basename, ...}

Language = Literal["python", "python-pcode"]

class Scratch2OtherFile(object):
    language: Language
    variables: List[VariableDict]
    funcs: List[Block]
    entries: List[Block]
    isStage: bool
    name: str
    counts: Dict[str, int]
    translator: WrappedTranslator
    target: Target
    blockToFuncName: Dict[Block, str]
    procedures_prototypes: Dict[str, dict]
    assets: AssetsDict

    def __init__(self, language: Language, name: str, target: Target, isStage: bool = ...):
        ...

    def getAssets(self) -> None:
        ...

    def getSpecialName(self, head: Block) -> tuple[str, dict]:
        ...

    def toCodeFrom(self, head: Block, with_comments: bool = ...) -> str:
        ...

    def getProceduresPrototypes(self) -> str:
        ...

    def getVariablesDict(self) -> str:
        ...

    def getFuncList(self) -> str:
        ...
    
    def getEntryList(self) -> str:
        ...

    def getClickFuncs(self) -> str:
        ...

    def getKeyFuncMap(self) -> str:
        ...

    def getBroadcastParams(self) -> str:
        ...

    def getBCFM(self) -> str:
        ...

    def getCheckerMap(self) -> str:
        ...

    def getSACFuncs(self) -> str:
        ...

    def getArgMap(self, args: dict[str, str]) -> str:
        ...

    def analyze(self, stage: Optional[Target] = None, print_progress: bool = ..., with_comments: bool = ..., with_variables: bool = ...) -> tuple[str, str]:
        ...

    def generate(self, output: Path, stage: Optional[Target] = None, print_progress: bool = ..., with_comments: bool = ..., with_variables: bool = ...) -> None:
        ...

class Scratch(object):
    project: Project
    public_id_to_variable_name: Dict[str, str]

    def __init__(self, project: Project):
        ...

    def analyze(self, language: Language="python", print_progress: bool = ..., with_comments: bool = ..., with_variables: bool = ...) -> tuple[dict[str, tuple[str, str]], tuple[str, str]]:
        ...

    def generate(self, output: Path | str, language: Language="python", print_progress: bool = ..., with_comments: bool = ..., with_variables: bool = ...) -> None:
        ...