import esphome.codegen as cg
from esphome.components import select
import esphome.config_validation as cv
from esphome.const import CONF_ID

from .. import CONF_DUCO_ID, DUCO_COMPONENT_SCHEMA

DEPENDENCIES = ["duco"]
CODEOWNERS = ["@kokx"]

DUCO_MODE_OPTIONS = [
    "AUTO",
    "MAN1",
    "MAN2",
    "MAN3",
    "EMPT",
    "CNT1",
    "CNT2",
    "CNT3",
    "MAN1x2",
    "MAN2x2",
    "MAN3x2",
    "MAN1x3",
    "MAN2x3",
    "MAN3x3",
]

CONF_BYPASS_MODE = "bypass_mode"

DUCO_BYPASS_MODE_OPTIONS = [
    "AUTO",
    "CLOSED",
    "OPEN",
]

duco_ns = cg.esphome_ns.namespace("duco")
DucoSelect = duco_ns.class_("DucoSelect", cg.PollingComponent, select.Select)
DucoBypassModeSelect = duco_ns.class_(
    "DucoBypassModeSelect", cg.PollingComponent, select.Select
)

CONFIG_SCHEMA = cv.All(
    select.select_schema(DucoSelect)
    .extend(cv.COMPONENT_SCHEMA)
    .extend(cv.polling_component_schema("3s"))
    .extend(DUCO_COMPONENT_SCHEMA)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(DucoSelect),
            cv.Optional(CONF_BYPASS_MODE): select.select_schema(DucoBypassModeSelect)
            .extend(cv.COMPONENT_SCHEMA)
            .extend(cv.polling_component_schema("60s"))
            .extend({cv.GenerateID(): cv.declare_id(DucoBypassModeSelect)}),
        }
    )
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_DUCO_ID])

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await select.register_select(var, config, options=DUCO_MODE_OPTIONS)
    cg.add(var.set_parent(parent))

    if CONF_BYPASS_MODE in config:
        bypass_mode_config = config[CONF_BYPASS_MODE]
        var = cg.new_Pvariable(bypass_mode_config[CONF_ID])
        await cg.register_component(var, bypass_mode_config)
        await select.register_select(var, bypass_mode_config, options=DUCO_BYPASS_MODE_OPTIONS)
        cg.add(var.set_parent(parent))
