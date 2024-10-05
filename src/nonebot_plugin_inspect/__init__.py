from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Command, UniMessage, Match, At, load_builtin_plugin
from nonebot_plugin_uninfo import Uninfo, QryItrface, Scene, SceneType
from nonebot_plugin_uninfo.constraint import SupportAdapter, SupportScope

from .i18n import Lang
load_builtin_plugin("lang")
__plugin_meta__ = PluginMetadata(
    "inspect",
    "Inspect on any user, group or channel",
    "/inspect",
    "application",
    "https://github.com/RF-Tar-Railt/nonebot-plugin-inspect",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_uninfo", "nonebot_plugin_alconna"),
)


matcher = (
    Command(
        "inspect [target:At]",
        Lang.nonebot_plugin_inspect.description()
    )
    .example("inspect @user\ninspect #channel\ninspect")
    .build(block=True, use_cmd_start=True, skip_for_unmatch=False)
)


SceneNames = {
    "PRIVATE": Lang.nonebot_plugin_inspect.scene.private,
    "GROUP": Lang.nonebot_plugin_inspect.scene.group,
    "GUILD": Lang.nonebot_plugin_inspect.scene.guild,
    "CHANNEL_TEXT": Lang.nonebot_plugin_inspect.scene.channel_text,
    "CHANNEL_VOICE": Lang.nonebot_plugin_inspect.scene.channel_voice,
    "CHANNEL_CATEGORY": Lang.nonebot_plugin_inspect.scene.channel_category,
}


@matcher.handle()
async def inspect(session: Uninfo, interface: QryItrface, target: Match[At]):
    adapter = session.adapter.value if isinstance(session.adapter, SupportAdapter) else str(session.adapter)
    scope = session.scope.value if isinstance(session.scope, SupportScope) else str(session.scope)
    texts = (
        UniMessage
        .i18n(Lang.nonebot_plugin_inspect.platform, adapter=adapter, scope=scope).text("\n")
        .i18n(Lang.nonebot_plugin_inspect.self, self_id=session.self_id).text("\n")
    )
    if target.available:
        at = target.result
        if at.flag == "user":
            texts.i18n(Lang.nonebot_plugin_inspect.user, user_id=at.target)
        elif at.flag == "channel":
            texts.i18n(Lang.nonebot_plugin_inspect.channel, channel_id=at.target)
        else:
            return await matcher.send(Lang.nonebot_plugin_inspect.invalid())
        return await matcher.send(texts)
    texts.i18n(Lang.nonebot_plugin_inspect.scene.name, scene=SceneNames[session.scene.type.name]()).text("\n")
    texts.i18n(Lang.nonebot_plugin_inspect.user, user_id=f"{session.user.name + ' | ' if session.user.name else ''}{session.user.id}").text("\n")
    if session.scene.parent:
        if session.scene.is_private:
            texts.i18n(
                Lang.nonebot_plugin_inspect.group, group_id=f"{session.scene.parent.name + ' | ' if session.scene.parent.name else ''}{session.scene.parent.id}"
            ).text("\n")
        else:
            texts.i18n(
                Lang.nonebot_plugin_inspect.guild, guild_id=f"{session.scene.parent.name + ' | ' if session.scene.parent.name else ''}{session.scene.parent.id}"
            ).text("\n")
    if session.scene.is_group:
        texts.i18n(
            Lang.nonebot_plugin_inspect.group, group_id=f"{session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
        )
    elif session.scene.is_guild:
        texts.i18n(
            Lang.nonebot_plugin_inspect.guild, guild_id=f"{session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
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
        texts.text("\n").i18n(
            Lang.nonebot_plugin_inspect.member, member_id=f"{session.member.nick + ' | ' if session.member.nick else ''}{session.member.id}"
        )
    await matcher.send(texts)
