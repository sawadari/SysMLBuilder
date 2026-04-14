package local.sysmlbuilder.cameo;

import java.io.File;
import java.lang.reflect.Method;
import java.util.Arrays;

import com.nomagic.magicdraw.commandline.CommandLineAction;
import com.nomagic.magicdraw.core.Application;
import com.nomagic.magicdraw.core.Project;
import com.nomagic.magicdraw.core.project.ProjectDescriptor;
import com.nomagic.magicdraw.core.project.ProjectDescriptorsFactory;
import com.nomagic.magicdraw.core.project.ProjectsManager;
import com.nomagic.magicdraw.plugins.Plugin;
import com.nomagic.magicdraw.plugins.PluginUtils;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package;

public final class CameoImportSmokeAction implements CommandLineAction {
    @Override
    public byte execute(String[] args) {
        try {
            Arguments parsed = Arguments.parse(args);
            ProjectsManager manager = Application.getInstance().getProjectsManager();
            Project project = manager.createProject();
            manager.setActiveProject(project);

            Object plugin = findPlugin("com.nomagic.magicdraw.emfuml2xmi.v5.EmfUml2XmiPlugin");
            Method importMethod = plugin.getClass().getMethod("imp0rt", String.class);
            importMethod.invoke(plugin, parsed.xmiPath().getAbsolutePath());

            Project activeProject = manager.getActiveProject();
            if (activeProject == null) {
                throw new IllegalStateException("No active project after import.");
            }

            File outputParent = parsed.outputPath().getAbsoluteFile().getParentFile();
            if (outputParent != null) {
                outputParent.mkdirs();
                activeProject.setDirectory(outputParent.getAbsolutePath());
            }
            activeProject.setFileName(parsed.outputPath().getName());
            activeProject.setName(stripExtension(parsed.outputPath().getName()));

            ProjectDescriptor descriptor = ProjectDescriptorsFactory.createLocalProjectDescriptor(activeProject, parsed.outputPath());
            if (!manager.saveProject(descriptor, true)) {
                throw new IllegalStateException("Failed to save imported project to " + parsed.outputPath());
            }

            Package primaryModel = activeProject.getPrimaryModel();
            int packagedElementCount = primaryModel == null ? -1 : primaryModel.getPackagedElement().size();
            System.out.println("CAMEO_IMPORT_OK");
            System.out.println("xmi=" + parsed.xmiPath().getAbsolutePath());
            System.out.println("project=" + parsed.outputPath().getAbsolutePath());
            System.out.println("packagedElements=" + packagedElementCount);

            manager.closeProject();
            return 0;
        } catch (Exception ex) {
            ex.printStackTrace(System.out);
            return 1;
        }
    }

    private Object findPlugin(String className) {
        for (Plugin plugin : PluginUtils.getPlugins()) {
            if (plugin != null && className.equals(plugin.getClass().getName())) {
                return plugin;
            }
        }
        throw new IllegalStateException("Required plugin not loaded: " + className);
    }

    private String stripExtension(String fileName) {
        int dot = fileName.lastIndexOf('.');
        return dot >= 0 ? fileName.substring(0, dot) : fileName;
    }

    private record Arguments(File xmiPath, File outputPath) {
        private static Arguments parse(String[] args) {
            File xmiPath = null;
            File outputPath = null;
            for (int index = 0; index < args.length; index++) {
                String arg = args[index];
                if ("--xmi".equals(arg) && index + 1 < args.length) {
                    xmiPath = new File(args[++index]);
                } else if ("--output".equals(arg) && index + 1 < args.length) {
                    outputPath = new File(args[++index]);
                }
            }
            if (xmiPath == null || outputPath == null) {
                throw new IllegalArgumentException(
                    "Usage: --xmi <input.xmi> --output <output.mdzip>. Args=" + Arrays.toString(args)
                );
            }
            return new Arguments(xmiPath, outputPath);
        }
    }
}
