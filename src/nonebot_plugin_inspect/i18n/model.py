# This file is @generated by tarina.lang CLI tool
# It is not intended for manual editing.

from tarina.lang.model import LangItem, LangModel


class NonebotPluginInspectScene:
    name: LangItem = LangItem("nonebot_plugin_inspect", "scene.name")
    private: LangItem = LangItem("nonebot_plugin_inspect", "scene.private")
    group: LangItem = LangItem("nonebot_plugin_inspect", "scene.group")
    guild: LangItem = LangItem("nonebot_plugin_inspect", "scene.guild")
    channel_text: LangItem = LangItem("nonebot_plugin_inspect", "scene.channel_text")
    channel_voice: LangItem = LangItem("nonebot_plugin_inspect", "scene.channel_voice")
    channel_category: LangItem = LangItem("nonebot_plugin_inspect", "scene.channel_category")



class NonebotPluginInspect:
    description: LangItem = LangItem("nonebot_plugin_inspect", "description")
    platform: LangItem = LangItem("nonebot_plugin_inspect", "platform")
    self: LangItem = LangItem("nonebot_plugin_inspect", "self")
    scene = NonebotPluginInspectScene
    user: LangItem = LangItem("nonebot_plugin_inspect", "user")
    channel: LangItem = LangItem("nonebot_plugin_inspect", "channel")
    group: LangItem = LangItem("nonebot_plugin_inspect", "group")
    guild: LangItem = LangItem("nonebot_plugin_inspect", "guild")
    private: LangItem = LangItem("nonebot_plugin_inspect", "private")
    member: LangItem = LangItem("nonebot_plugin_inspect", "member")
    invalid: LangItem = LangItem("nonebot_plugin_inspect", "invalid")


class Lang(LangModel):
    nonebot_plugin_inspect = NonebotPluginInspect
