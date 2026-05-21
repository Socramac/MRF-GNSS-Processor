def classFactory(iface):
    from .plugin import MrfGnssProcessorPlugin
    return MrfGnssProcessorPlugin(iface)
