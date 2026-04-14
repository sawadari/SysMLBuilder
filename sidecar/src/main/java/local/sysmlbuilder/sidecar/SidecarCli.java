package local.sysmlbuilder.sidecar;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import org.yaml.snakeyaml.Yaml;

public final class SidecarCli {
    private SidecarCli() {
    }

    public static void main(String[] args) throws Exception {
        CliArguments cli = CliArguments.parse(args);
        Map<String, Object> request = readYaml(cli.input());
        String target = requireString(request, "target");
        @SuppressWarnings("unchecked")
        Map<String, Object> model = (Map<String, Object>) request.get("model");
        if (model == null) {
            throw new IllegalArgumentException("Missing 'model' in request payload");
        }

        Uml2XmiExporter exporter = new Uml2XmiExporter();
        exporter.export(model, target, cli.output());
        System.out.println(cli.output());
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> readYaml(Path path) throws IOException {
        Yaml yaml = new Yaml();
        try (InputStream in = Files.newInputStream(path)) {
            Object loaded = yaml.load(in);
            if (!(loaded instanceof Map<?, ?> map)) {
                throw new IllegalArgumentException("Expected top-level mapping in " + path);
            }
            return (Map<String, Object>) map;
        }
    }

    private static String requireString(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (!(value instanceof String text) || text.isBlank()) {
            throw new IllegalArgumentException("Missing required string field: " + key);
        }
        return text;
    }

    private record CliArguments(Path input, Path output) {
        private static CliArguments parse(String[] args) {
            Path input = null;
            Path output = null;
            for (int i = 0; i < args.length; i++) {
                String arg = args[i];
                if ("--input".equals(arg) && i + 1 < args.length) {
                    input = Path.of(args[++i]);
                } else if ("--output".equals(arg) && i + 1 < args.length) {
                    output = Path.of(args[++i]);
                }
            }
            if (input == null || output == null) {
                throw new IllegalArgumentException("Usage: java -jar sidecar.jar --input request.yaml --output model.xmi");
            }
            return new CliArguments(input, output);
        }
    }
}
