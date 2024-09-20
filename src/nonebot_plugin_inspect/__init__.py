from nonebot import on_command
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_uninfo")

from nonebot_plugin_uninfo import Uninfo


__plugin_meta__ = PluginMetadata(
    "inspect",
    "Inspect on any user, group or channel",
    "/inspect",
    "application",
    "https://github.com/RF-Tar-Railt/nonebot-plugin-inspect",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_uninfo")
)


matcher = on_command("inspect", priority=1, block=True)

@matcher.handle()
async def inspect(session: Uninfo):
    texts = [
        f"平台名: {session.adapter} | {session.scope}",
        f"用户ID: {session.user.name + ' | ' if session.user.name else ''}{session.user.id}",
        f"自身ID: {session.self_id}",
        f"事件场景: {session.scene.type.name}",
        f"频道 ID: {session.scene.name + ' | ' if session.scene.name else ''}{session.scene.id}"
    ]
    if session.scene.parent:
        texts.append(f"群组 ID: {session.scene.parent.name + ' | ' if session.scene.parent.name else ''}{session.scene.parent.id}")
    if session.member:
        texts.append(f"成员 ID: {session.member.nick + ' | ' if session.member.nick else ''}{session.member.id}")
    await matcher.send("\n".join(texts))
