package local.sysmlbuilder.sidecar;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.XMLResource;
import org.eclipse.uml2.uml.AggregationKind;
import org.eclipse.uml2.uml.Class;
import org.eclipse.uml2.uml.Connector;
import org.eclipse.uml2.uml.ConnectorEnd;
import org.eclipse.uml2.uml.DataType;
import org.eclipse.uml2.uml.Dependency;
import org.eclipse.uml2.uml.Model;
import org.eclipse.uml2.uml.Package;
import org.eclipse.uml2.uml.Port;
import org.eclipse.uml2.uml.Property;
import org.eclipse.uml2.uml.Region;
import org.eclipse.uml2.uml.State;
import org.eclipse.uml2.uml.StateMachine;
import org.eclipse.uml2.uml.Transition;
import org.eclipse.uml2.uml.Type;
import org.eclipse.uml2.uml.UMLFactory;
import org.eclipse.uml2.uml.UMLPackage;
import org.eclipse.uml2.uml.resource.UMLResource;

final class Uml2XmiExporter {
    private final UMLFactory factory = UMLFactory.eINSTANCE;

    @SuppressWarnings("unchecked")
    void export(Map<String, Object> modelPayload, String target, Path outputPath) throws IOException {
        Files.createDirectories(outputPath.toAbsolutePath().getParent());
        Path rawOutputPath = outputPath.resolveSibling(outputPath.getFileName().toString() + ".raw");

        String packageName = stringValue(modelPayload.get("package_name"), "package_name");
        Model root = factory.createModel();
        root.setName(packageName);

        Package valueTypesPkg = root.createNestedPackage("ValueTypes");
        Package interfacesPkg = root.createNestedPackage("Interfaces");
        Package requirementsPkg = root.createNestedPackage("Requirements");
        Package blocksPkg = root.createNestedPackage("Blocks");
        Package relationshipsPkg = root.createNestedPackage("Relationships");

        Map<String, Type> typesByName = new HashMap<>();
        Map<String, Class> blocksByName = new HashMap<>();
        Map<String, Property> partProperties = new HashMap<>();
        Map<String, Port> portsByQualifiedName = new HashMap<>();
        Map<String, Class> requirementsByName = new HashMap<>();

        for (String valueTypeName : stringList(modelPayload.get("value_types"))) {
            DataType dataType = (DataType) valueTypesPkg.createPackagedElement(valueTypeName, UMLPackage.Literals.DATA_TYPE);
            typesByName.put(valueTypeName, dataType);
        }

        for (Map<String, Object> ifacePayload : mapList(modelPayload.get("interface_blocks"))) {
            Class interfaceBlock = interfacesPkg.createOwnedClass(stringValue(ifacePayload.get("name"), "interface_blocks.name"), false);
            typesByName.put(interfaceBlock.getName(), interfaceBlock);
            for (Map<String, Object> flowPropertyPayload : mapList(ifacePayload.get("flow_properties"))) {
                Property property = interfaceBlock.createOwnedAttribute(
                    stringValue(flowPropertyPayload.get("name"), "flow_properties.name"),
                    typesByName.get(stringValue(flowPropertyPayload.get("item_type"), "flow_properties.item_type"))
                );
                property.setIsReadOnly(false);
            }
        }

        for (Map<String, Object> requirementPayload : mapList(modelPayload.get("requirements"))) {
            Class requirementClass = requirementsPkg.createOwnedClass(stringValue(requirementPayload.get("name"), "requirements.name"), false);
            requirementClass.createOwnedComment().setBody(stringValue(requirementPayload.get("text"), "requirements.text"));
            requirementsByName.put(requirementClass.getName(), requirementClass);
        }

        for (Map<String, Object> blockPayload : mapList(modelPayload.get("blocks"))) {
            Class block = blocksPkg.createOwnedClass(stringValue(blockPayload.get("name"), "blocks.name"), false);
            blocksByName.put(block.getName(), block);
            typesByName.put(block.getName(), block);
        }

        for (Map<String, Object> blockPayload : mapList(modelPayload.get("blocks"))) {
            Class block = blocksByName.get(stringValue(blockPayload.get("name"), "blocks.name"));

            for (Map<String, Object> portPayload : mapList(blockPayload.get("ports"))) {
                String portName = stringValue(portPayload.get("name"), "ports.name");
                String portTypeName = stringValue(portPayload.get("type"), "ports.type");
                Type portType = typesByName.get(portTypeName);
                Port port = factory.createPort();
                port.setName(portName);
                port.setType(portType);
                block.getOwnedAttributes().add(port);
                portsByQualifiedName.put(block.getName() + "." + portName, port);
            }

            for (Map<String, Object> partPayload : mapList(blockPayload.get("parts"))) {
                String partName = stringValue(partPayload.get("name"), "parts.name");
                String typeName = stringValue(partPayload.get("type"), "parts.type");
                Type partType = typesByName.get(typeName);
                Property property = block.createOwnedAttribute(partName, partType);
                property.setAggregation(AggregationKind.COMPOSITE_LITERAL);
                partProperties.put(block.getName() + "." + partName, property);
            }

            for (Map<String, Object> stateMachinePayload : mapList(blockPayload.get("state_machines"))) {
                StateMachine stateMachine = (StateMachine) block.createOwnedBehavior(
                    stringValue(stateMachinePayload.get("name"), "state_machines.name"),
                    UMLPackage.Literals.STATE_MACHINE
                );
                Region region = stateMachine.createRegion("region");
                Map<String, State> states = new HashMap<>();
                for (String stateName : stringList(stateMachinePayload.get("states"))) {
                    State state = (State) region.createSubvertex(stateName, UMLPackage.Literals.STATE);
                    states.put(stateName, state);
                }
                for (Map<String, Object> transitionPayload : mapList(stateMachinePayload.get("transitions"))) {
                    Transition transition = region.createTransition(null);
                    transition.setName(
                        stringValue(transitionPayload.get("source"), "transitions.source")
                            + "_to_"
                            + stringValue(transitionPayload.get("target"), "transitions.target")
                    );
                    transition.setSource(states.get(stringValue(transitionPayload.get("source"), "transitions.source")));
                    transition.setTarget(states.get(stringValue(transitionPayload.get("target"), "transitions.target")));
                }
            }
        }

        for (Map<String, Object> connectorPayload : mapList(modelPayload.get("connectors"))) {
            String name = stringValue(connectorPayload.get("name"), "connectors.name");
            Endpoint source = resolveEndpoint(stringValue(connectorPayload.get("source"), "connectors.source"), partProperties, portsByQualifiedName);
            Endpoint targetEndpoint = resolveEndpoint(stringValue(connectorPayload.get("target"), "connectors.target"), partProperties, portsByQualifiedName);
            Class owner = blocksByName.get(source.ownerBlock());
            if (owner == null) {
                continue;
            }
            Connector connector = owner.createOwnedConnector(name);
            attachConnectorEnd(connector, source);
            attachConnectorEnd(connector, targetEndpoint);
        }

        for (Map<String, Object> relationshipPayload : mapList(modelPayload.get("relationships"))) {
            String kind = stringValue(relationshipPayload.get("kind"), "relationships.kind");
            String name = stringValue(relationshipPayload.get("name"), "relationships.name");
            if ("satisfy".equals(kind)) {
                Dependency dependency = (Dependency) relationshipsPkg.createPackagedElement(name, UMLPackage.Literals.DEPENDENCY);
                addClientSupplier(
                    dependency,
                    resolveRequirementOrBlock(stringValue(relationshipPayload.get("client"), "relationships.client"), blocksByName, requirementsByName),
                    resolveRequirementOrBlock(stringValue(relationshipPayload.get("supplier"), "relationships.supplier"), blocksByName, requirementsByName)
                );
            } else if ("allocate".equals(kind)) {
                Dependency dependency = (Dependency) relationshipsPkg.createPackagedElement(name, UMLPackage.Literals.DEPENDENCY);
                addClientSupplier(
                    dependency,
                    resolveRequirementOrBlock(stringValue(relationshipPayload.get("client"), "relationships.client"), blocksByName, requirementsByName),
                    resolveRequirementOrBlock(stringValue(relationshipPayload.get("supplier"), "relationships.supplier"), blocksByName, requirementsByName)
                );
            }
        }

        root.createOwnedComment().setBody("Generated by SysMLBuilder sidecar for target=" + target);
        saveModel(root, rawOutputPath);
        XmiTargetShim.forTarget(target).apply(rawOutputPath, outputPath, modelPayload);
        Files.deleteIfExists(rawOutputPath);
    }

    private void addClientSupplier(Dependency dependency, org.eclipse.uml2.uml.NamedElement client, org.eclipse.uml2.uml.NamedElement supplier) {
        if (client != null) {
            dependency.getClients().add(client);
        }
        if (supplier != null) {
            dependency.getSuppliers().add(supplier);
        }
    }

    private org.eclipse.uml2.uml.NamedElement resolveRequirementOrBlock(
        String rawPath,
        Map<String, Class> blocksByName,
        Map<String, Class> requirementsByName
    ) {
        String name = localName(rawPath);
        if (requirementsByName.containsKey(name)) {
            return requirementsByName.get(name);
        }
        if (blocksByName.containsKey(name)) {
            return blocksByName.get(name);
        }
        String[] segments = rawPath.split("::");
        if (segments.length > 1) {
            String candidate = segments[segments.length - 1];
            return blocksByName.getOrDefault(candidate, requirementsByName.get(candidate));
        }
        return null;
    }

    private void attachConnectorEnd(Connector connector, Endpoint endpoint) {
        ConnectorEnd end = connector.createEnd();
        end.setPartWithPort(endpoint.part());
        end.setRole(endpoint.port());
    }

    private Endpoint resolveEndpoint(
        String rawPath,
        Map<String, Property> partProperties,
        Map<String, Port> portsByQualifiedName
    ) {
        String[] segments = rawPath.split("\\.");
        if (segments.length < 3) {
            throw new IllegalArgumentException("Connector endpoint must look like Root.part.port: " + rawPath);
        }
        String ownerBlock = localName(segments[0]);
        String partName = segments[1];
        String portName = segments[2];
        Property part = partProperties.get(ownerBlock + "." + partName);
        if (part == null || part.getType() == null) {
            throw new IllegalArgumentException("Unknown part endpoint: " + rawPath);
        }
        Port port = portsByQualifiedName.get(localName(part.getType().getName()) + "." + portName);
        if (port == null) {
            throw new IllegalArgumentException("Unknown port endpoint: " + rawPath);
        }
        return new Endpoint(ownerBlock, part, port);
    }

    private void saveModel(Model root, Path outputPath) throws IOException {
        ResourceSet resourceSet = new ResourceSetImpl();
        resourceSet.getPackageRegistry().put(UMLPackage.eNS_URI, UMLPackage.eINSTANCE);
        resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put(UMLResource.FILE_EXTENSION, UMLResource.Factory.INSTANCE);
        resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put(Resource.Factory.Registry.DEFAULT_EXTENSION, UMLResource.Factory.INSTANCE);

        URI uri = URI.createFileURI(outputPath.toAbsolutePath().toString());
        Resource resource = resourceSet.createResource(uri, UMLResource.UML_CONTENT_TYPE_IDENTIFIER);
        resource.getContents().add(root);
        Map<Object, Object> options = new HashMap<>();
        options.put(XMLResource.OPTION_ENCODING, "UTF-8");
        resource.save(options);
    }

    private List<Map<String, Object>> mapList(Object value) {
        List<Map<String, Object>> items = new ArrayList<>();
        if (value instanceof List<?> list) {
            for (Object entry : list) {
                if (entry instanceof Map<?, ?> map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> typed = (Map<String, Object>) map;
                    items.add(typed);
                }
            }
        }
        return items;
    }

    private List<String> stringList(Object value) {
        List<String> items = new ArrayList<>();
        if (value instanceof List<?> list) {
            for (Object entry : list) {
                if (entry != null) {
                    items.add(String.valueOf(entry));
                }
            }
        }
        return items;
    }

    private String stringValue(Object value, String field) {
        if (value == null) {
            throw new IllegalArgumentException("Missing field: " + field);
        }
        String text = String.valueOf(value);
        if (text.isBlank()) {
            throw new IllegalArgumentException("Blank field: " + field);
        }
        return text;
    }

    private String localName(String path) {
        int sep = path.lastIndexOf("::");
        return sep >= 0 ? path.substring(sep + 2) : path;
    }

    private record Endpoint(String ownerBlock, Property part, Port port) {
    }
}
