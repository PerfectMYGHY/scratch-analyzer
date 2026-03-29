import Scratch4Python as Scratch
# 初始化函数
def init():
    default_instance = Scratch.Instance("{name}", {variables}, {x}, {y}, {direction}, {visible}, {size}, {currentCostume},
                                        {funcs}, {entries}, {assets}, {broadcast_params}, {layer_order}, {volume},
                                        {click_funcs}, {key_map}, {backdrop_change_func_map}, {checker_map},
                                        {start_as_clone_funcs}, {procedures_prototypes})
    Scratch.register(default_instance)
