from typing import TypedDict, List, Optional, Dict, Any, Union

from .translator import WrappedTranslator


class MetaDict(TypedDict):
    semver: str
    vm: str
    agent: str

class MonitorParamDict(TypedDict):
    VARIABLE: str
    LIST: str

class MonitorDict(TypedDict):
    id: str
    mode: str
    opcode: str
    params: MonitorParamDict
    spriteName: Optional[str]
    value: Any
    width: int
    height: int
    x: float
    y: float
    visible: bool
    sliderMin: Optional[float]
    sliderMax: Optional[float]
    isDiscrete: Optional[bool]

ValueInput = List[int, List[int , Any]] # type: ignore
CodeInput = List[int, str, List[int , Any]] # type: ignore
FieldInput = List[int, str, ...] # type: ignore
InputsDict = Dict[str, Union[ValueInput, CodeInput, FieldInput]]
FieldsDict = Dict[str, List[str, Optional[str]]] # type: ignore

class BlockDict(TypedDict):
    opcode: str
    next: Optional[str]
    parent: Optional[str]
    inputs: InputsDict
    fields: FieldsDict
    shadow: bool
    topLevel: bool
    comment: Optional[str]
    mutation: Optional[dict]

VariablesDict = Dict[str, List[str, Any]] # type: ignore
ListsDict = Dict[str, List[str, Any]] # type: ignore
BroadcastsDict = Dict[str, str]
BlocksDict = Dict[str, BlockDict]

class Comment(TypedDict):
    blockId: Optional[str]
    x: float
    y: float
    width: float
    height: float
    minimized: bool
    text: str

CommentsDict = Dict[str, Comment]

class CostumeDict(TypedDict):
    name: str
    bitmapResolution: int
    dataFormat: str
    assetId: str
    md5ext: str
    rotationCenterX: float
    rotationCenterY: float

class Sound(TypedDict):
    name: str
    assetId: str
    dataFormat: str
    rate: int
    sampleCount: int
    md5ext: str

class TargetDict(TypedDict):
    isStage: bool
    name: str
    variables: VariablesDict
    lists: ListsDict
    broadcasts: BroadcastsDict
    blocks: BlocksDict
    comments: CommentsDict
    currentCostume: int
    costumes: List[CostumeDict]
    sounds: List[Sound]
    volume: int
    layerOrder: int
    visible: Optional[bool]
    x: Optional[float]
    y: Optional[float]
    size: Optional[float]
    direction: Optional[float]
    draggable: Optional[bool]
    rotationStyle: Optional[Any]
    tempo: Optional[int]
    ...

class ProjectDict(TypedDict):
    targets: List[TargetDict]
    monitors: List[MonitorDict]
    extensions: List[str]
    extensionURLs: Optional[Dict[str, str]]
    meta: MetaDict

# =========================

class Input(object):
    data: list
    target: Target
    name: str

    def __init__(self, _input: list, target: Target, name: str):
        ...

    def toCode(self, translator: WrappedTranslator, func_name: str, procedures_prototypes: dict[str, dict]) -> str:
        ...

class Field(object):
    data: list
    target: Target

    def __init__(self, field: list, target: Target):
        ...

    def toCode(self, translator: WrappedTranslator) -> str:
        ...

class Block(object):
    opcode: str
    _next: Optional[str]
    next: Optional[Block]
    _parent: Optional[str]
    parent: Optional[Block]
    _inputs: InputsDict
    inputs: Dict[str, Input]
    _fields: FieldsDict
    fields: Dict[str, Field]
    shadow: bool
    topLevel: bool
    target: Target
    computed: bool
    comment: Optional[str]
    data: BlockDict

    def __init__(self, block: BlockDict, target: Target):
        ...

    def getComment(self, indent: int, translator: WrappedTranslator, uniqueEnv: bool = ..., with_comments: bool = ...) -> str:
        ...

    def compute_relation(self):
        ...

    def generateArgs(self, arg_ids: list[str], args: dict[str, Input], translator: WrappedTranslator, func_name: str, procedures_prototypes: dict[str, dict]) -> str:
        ...

    def toCode(self, translator: WrappedTranslator, indent: int, func_name: str, procedures_prototypes: dict[str, dict], with_comments: bool = ...) -> tuple[str, int]:
        ...

class Target(object):
    isStage: bool
    name: str
    variables: VariablesDict
    lists: ListsDict
    broadcasts: BroadcastsDict
    _blocks: BlocksDict
    blocks: Dict[str, Block]
    comments: CommentsDict
    currentCostume: int
    costumes: List[CostumeDict]
    sounds: List[Sound]
    volume: int
    layerOrder: int
    visible: Optional[bool]
    x: Optional[float]
    y: Optional[float]
    size: Optional[float]
    direction: Optional[float]
    draggable: Optional[bool]
    rotationStyle: Optional[Any]
    tempo: Optional[int]
    args: Dict[str, Any]

    def __init__(self, target: TargetDict, print_progress: bool = ...):
        ...

class Monitor(object):
    id: str
    mode: str
    opcode: str
    params: MonitorParamDict
    spriteName: Optional[str]
    value: Any
    width: int
    height: int
    x: float
    y: float
    visible: bool
    sliderMin: Optional[float]
    sliderMax: Optional[float]
    isDiscrete: Optional[bool]

    def __init__(self, monitor: MonitorDict):
        ...

class Extension(object):
    def __init__(self, extension: str):
        ...

class Meta(object):
    semver: str
    vm: str
    agent: str

    def __init__(self, meta: MetaDict):
        ...

class Project(object):
    project: ProjectDict
    targets: Dict[str, Target]
    monitors: Dict[str, Monitor]
    extensions: Dict[str, Extension]
    meta: Meta

    def __init__(self, project: ProjectDict, print_progress: bool = ...):
        ...

    def _parse(self, print_progress: bool = ...) -> None:
        ...