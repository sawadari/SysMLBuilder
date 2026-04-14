package local.sysmlbuilder.cameo;

import com.nomagic.magicdraw.commandline.CommandLineActionManager;
import com.nomagic.magicdraw.plugins.Plugin;

public final class CameoImportSmokePlugin extends Plugin {
    @Override
    public void init() {
        CommandLineActionManager.getInstance().addAction(new CameoImportSmokeAction());
    }

    @Override
    public boolean close() {
        return true;
    }

    @Override
    public boolean isSupported() {
        return true;
    }
}
