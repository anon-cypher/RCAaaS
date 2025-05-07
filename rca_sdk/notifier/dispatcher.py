from rca_sdk.utils.plugin_loader import load_plugin # adjust path if needed

def dispatch(message, channels):
    for name, config in channels.items():
        # print(f"Dispatching to {name}: {message}")
        try:
            plugin = load_plugin(f"rca_sdk.plugins.notifications.{name}")
            plugin.send(message, config)
        except Exception as e:
            print(f"[❌ Failed to dispatch to {name}]: {e}")
