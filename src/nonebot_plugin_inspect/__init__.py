from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Command, UniMessage
from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_uninfo.constraint import SupportAdapter, SupportScope

from .i18n import Lang

__plugin_meta__ = PluginMetadata(
    "inspect",
    "Inspect on any user, group or channel",
    "/inspect",
    "application",
    "https://github.com/RF-Tar-Railt/nonebot-plugin-inspect",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_uninfo", "nonebot_plugin_alconna"),
)


matcher = Command("inspect").build(priority=1, block=True)


SceneNames = {
    "PRIVATE": Lang.nonebot_plugin_inspect.scene.private(),
    "GROUP": Lang.nonebot_plugin_inspect.scene.group(),
    "GUILD": Lang.nonebot_plugin_inspect.scene.guild(),
    "CHANNEL_TEXT": Lang.nonebot_plugin_inspect.scene.channel_text(),
    "CHANNEL_VOICE": Lang.nonebot_plugin_inspect.scene.channel_voice(),
    "CHANNEL_CATEGORY": Lang.nonebot_plugin_inspect.scene.channel_category(),
}


@matcher.handle()
async def inspect(session: Uninfo):
    adapter = session.adapter.value if isinstance(session.adapter, SupportAdapter) else str(session.adapter)
    scope = session.scope.value if isinstance(session.scope, SupportScope) else str(session.scope)
    texts = (
        UniMessage
        .i18n(Lang.nonebot_plugin_inspect.platform, adapter=adapter, scope=scope)
        .i18n(Lang.nonebot_plugin_inspect.self, self_id=session.self_id)
        .i18n(Lang.nonebot_plugin_inspect.user, user_id=f"{session.user.name + ' | ' if session.user.name else ''}{session.user.id}")
        .i18n(Lang.nonebot_plugin_inspect.scene.name, scene=SceneNames[session.scene.type.name])
    )
    if session.scene.parent:
        if session.scene.is_private:
            texts.i18n(
                Lang.nonebot_plugin_inspect.group, group_id=f"{session.scene.parent.name + ' | ' if session.scene.parent.name else ''}{session.scene.parent.id}"
            )
        else:
            texts.i18n(
                Lang.nonebot_plugin_inspect.guild, channel_id=f"{session.scene.parent.name + ' | ' if session.scene.parent.name else ''}{session.scene.parent.id}"
            )
    if session.scene.is_group:
        texts.i18n(
            Lang.nonebot_plugin_inspect.group, group_id=f"{session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
        )
    elif session.scene.is_guild:
        texts.i18n(
            Lang.nonebot_plugin_inspect.guild, channel_id=f"{session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
        )
    elif session.scene.is_private:
        texts.i18n(
            Lang.nonebot_plugin_inspect.private, private_id=f"{session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
        )
    else:
        texts.i18n(
            Lang.nonebot_plugin_inspect.channel, channel_id=f"{session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
        )
    if session.member:
        texts.i18n(
            Lang.nonebot_plugin_inspect.member, member_id=f"{session.member.nick + ' | ' if session.member.nick else ''}{session.member.id}"
        )
    await matcher.send(texts)
