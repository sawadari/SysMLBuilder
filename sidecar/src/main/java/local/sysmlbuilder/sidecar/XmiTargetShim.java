package local.sysmlbuilder.sidecar;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Map;

interface XmiTargetShim {
    void apply(Path rawXmiPath, Path outputPath, Map<String, Object> modelPayload) throws IOException;

    static XmiTargetShim forTarget(String target) {
        return switch (target) {
            case "cameo" -> new WrappedXmiTargetShim(
                "2.5",
                "http://www.omg.org/spec/XMI/20131001",
                "http://www.omg.org/spec/UML/20161101",
                "http://www.omg.org/spec/SysML/20161101/SysML.xmi",
                false
            );
            case "ea" -> new WrappedXmiTargetShim(
                "2.1",
                "http://schema.omg.org/spec/XMI/2.1",
                "http://schema.omg.org/spec/UML/2.1",
                "http://www.omg.org/spec/SysML/20161101/SysML.xmi",
                true
            );
            default -> throw new IllegalArgumentException("Unsupported target: " + target);
        };
    }
}
