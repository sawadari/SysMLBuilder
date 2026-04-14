package local.sysmlbuilder.sidecar;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

final class WrappedXmiTargetShim implements XmiTargetShim {
    private static final String PROFILE_HREF = "http://www.omg.org/spec/SysML/20161101/SysML.xmi#SysML";
    private static final String ECORE_NS = "http://www.eclipse.org/emf/2002/Ecore";

    private final String xmiVersion;
    private final String xmiNs;
    private final String umlNs;
    private final String sysmlNs;
    private final boolean includeEaDocumentation;

    WrappedXmiTargetShim(String xmiVersion, String xmiNs, String umlNs, String sysmlNs, boolean includeEaDocumentation) {
        this.xmiVersion = xmiVersion;
        this.xmiNs = xmiNs;
        this.umlNs = umlNs;
        this.sysmlNs = sysmlNs;
        this.includeEaDocumentation = includeEaDocumentation;
    }

    @Override
    public void apply(Path rawXmiPath, Path outputPath, Map<String, Object> modelPayload) throws IOException {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setNamespaceAware(true);
            Document raw = factory.newDocumentBuilder().parse(Files.newInputStream(rawXmiPath));
            Document wrapped = factory.newDocumentBuilder().newDocument();

            Element xmiRoot = wrapped.createElementNS(xmiNs, "xmi:XMI");
            xmiRoot.setAttributeNS(XMLConstants.XMLNS_ATTRIBUTE_NS_URI, "xmlns:xmi", xmiNs);
            xmiRoot.setAttributeNS(XMLConstants.XMLNS_ATTRIBUTE_NS_URI, "xmlns:uml", umlNs);
            xmiRoot.setAttributeNS(XMLConstants.XMLNS_ATTRIBUTE_NS_URI, "xmlns:sysml", sysmlNs);
            xmiRoot.setAttributeNS(XMLConstants.XMLNS_ATTRIBUTE_NS_URI, "xmlns:ecore", ECORE_NS);
            xmiRoot.setAttributeNS(xmiNs, "xmi:version", xmiVersion);
            wrapped.appendChild(xmiRoot);

            if (includeEaDocumentation) {
                Element documentation = wrapped.createElementNS(xmiNs, "xmi:Documentation");
                documentation.setAttribute("exporter", "SysMLBuilder sidecar");
                documentation.setAttribute("exporterVersion", "0.1.0");
                xmiRoot.appendChild(documentation);
            }

            Element importedModel = (Element) wrapped.importNode(raw.getDocumentElement(), true);
            wrapped.renameNode(importedModel, umlNs, "uml:Model");
            normalizeXmiNamespace(importedModel);
            importedModel.removeAttributeNS(xmiNs, "version");
            importedModel.removeAttribute("xmlns:xmi");
            importedModel.removeAttribute("xmlns:uml");
            xmiRoot.appendChild(importedModel);

            appendProfileApplication(wrapped, importedModel);
            appendStereotypes(wrapped, xmiRoot, importedModel, modelPayload);
            appendDiagrams(wrapped, xmiRoot, importedModel, modelPayload);

            Transformer transformer = TransformerFactory.newInstance().newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
            Files.createDirectories(outputPath.toAbsolutePath().getParent());
            try (OutputStream out = Files.newOutputStream(outputPath)) {
                transformer.transform(new DOMSource(wrapped), new StreamResult(out));
            }
        } catch (Exception ex) {
            throw new IOException("Failed to apply target shim", ex);
        }
    }

    private void normalizeXmiNamespace(Element root) {
        normalizeXmiAttributes(root);
        NodeList children = root.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element) {
                normalizeXmiNamespace(element);
            }
        }
    }

    private void normalizeXmiAttributes(Element element) {
        moveXmiAttribute(element, "id");
        moveXmiAttribute(element, "type");
        moveXmiAttribute(element, "version");
    }

    private void moveXmiAttribute(Element element, String localName) {
        String value = element.getAttributeNS(xmiNs, localName);
        if (!value.isBlank()) {
            return;
        }
        if (element.hasAttribute("xmi:" + localName)) {
            value = element.getAttribute("xmi:" + localName);
            element.removeAttribute("xmi:" + localName);
        }
        if (!value.isBlank()) {
            element.setAttributeNS(xmiNs, "xmi:" + localName, value);
        }
    }

    private void appendProfileApplication(Document document, Element model) {
        String modelId = model.getAttributeNS(xmiNs, "id");
        if (modelId.isBlank()) {
            return;
        }
        Element profileApplication = document.createElement("profileApplication");
        profileApplication.setAttributeNS(xmiNs, "xmi:type", "uml:ProfileApplication");
        profileApplication.setAttributeNS(xmiNs, "xmi:id", stereotypeId("profileApplication", modelId));
        profileApplication.setAttribute("applyingPackage", modelId);

        Element extension = document.createElementNS(xmiNs, "xmi:Extension");
        extension.setAttribute("extender", ECORE_NS);
        Element annotation = document.createElementNS(ECORE_NS, "ecore:EAnnotation");
        annotation.setAttributeNS(xmiNs, "xmi:id", stereotypeId("eAnnotation", modelId));
        annotation.setAttribute("source", "http://www.eclipse.org/uml2/2.0.0/UML");
        Element references = document.createElement("references");
        references.setAttributeNS(xmiNs, "xmi:type", "ecore:EPackage");
        references.setAttribute("href", PROFILE_HREF);
        annotation.appendChild(references);
        extension.appendChild(annotation);
        profileApplication.appendChild(extension);

        Element appliedProfile = document.createElement("appliedProfile");
        appliedProfile.setAttributeNS(xmiNs, "xmi:type", "uml:Profile");
        appliedProfile.setAttribute("href", PROFILE_HREF);
        profileApplication.appendChild(appliedProfile);
        model.appendChild(profileApplication);
    }

    private void appendStereotypes(Document document, Element root, Element model, Map<String, Object> modelPayload) {
        appendValueTypes(document, root, model, stringList(modelPayload.get("value_types")));
        appendInterfaceBlocks(document, root, model, mapList(modelPayload.get("interface_blocks")));
        appendRequirements(document, root, model, mapList(modelPayload.get("requirements")));
        appendBlocks(document, root, model, mapList(modelPayload.get("blocks")));
        appendRelationships(document, root, model, mapList(modelPayload.get("relationships")));
    }

    private void appendDiagrams(Document document, Element root, Element model, Map<String, Object> modelPayload) {
        Element extension = document.createElementNS(xmiNs, "xmi:Extension");
        extension.setAttribute("extender", includeEaDocumentation ? "Enterprise Architect" : "SysMLBuilder");
        if (includeEaDocumentation) {
            extension.setAttribute("extenderID", "6.5");
        }
        root.appendChild(extension);

        Element diagrams = document.createElement("diagrams");
        extension.appendChild(diagrams);

        int localId = 1;
        localId = appendStateMachineDiagrams(document, diagrams, model, mapList(modelPayload.get("blocks")), localId);
        localId = appendBlockDefinitionDiagram(document, diagrams, model, mapList(modelPayload.get("blocks")), localId);
        localId = appendInternalBlockDiagram(document, diagrams, model, mapList(modelPayload.get("blocks")), mapList(modelPayload.get("connectors")), localId);
        appendRequirementDiagram(document, diagrams, model, mapList(modelPayload.get("requirements")), localId);
    }

    private int appendStateMachineDiagrams(
        Document document,
        Element diagrams,
        Element model,
        List<Map<String, Object>> blocks,
        int localId
    ) {
        Element blocksPackage = findPackagedElement(model, "Blocks");
        String blocksPackageId = xmiId(blocksPackage);
        for (Map<String, Object> blockPayload : blocks) {
            Element block = findPackagedElement(blocksPackage, stringValue(blockPayload.get("name")));
            for (Map<String, Object> stateMachinePayload : mapList(blockPayload.get("state_machines"))) {
                String stateMachineName = stringValue(stateMachinePayload.get("name"));
                Element stateMachine = findOwnedBehavior(block, stateMachineName);
                String stateMachineId = xmiId(stateMachine);
                Element region = findFirstChild(stateMachine, "region");
                List<Element> elements = new ArrayList<>();

                List<String> states = stringList(stateMachinePayload.get("states"));
                int[][] positions = new int[][] {
                    {60, 60}, {190, 220}, {358, 106}, {220, 60}, {380, 240}
                };
                List<String> stateDuids = new ArrayList<>();
                for (int index = 0; index < states.size(); index++) {
                    String stateName = states.get(index);
                    Element state = findSubvertex(region, stateName);
                    int[] position = positions[index % positions.length];
                    String duid = duid(stateMachineName + "." + stateName).toUpperCase();
                    stateDuids.add(duid);
                    elements.add(diagramElement(
                        document,
                        "Left=" + position[0] + ";Top=" + position[1] + ";Right=" + (position[0] + 120) + ";Bottom=" + (position[1] + 60) + ";",
                        xmiId(state),
                        index + 1,
                        "DUID=" + duid + ";NSL=0;"
                    ));
                }
                elements.add(diagramElement(
                    document,
                    "Left=10;Top=10;Right=515;Bottom=319;",
                    stateMachineId,
                    elements.size() + 1,
                    "DUID=" + duid(stateMachineName).toUpperCase() + ";NSL=1;"
                ));
                for (Map<String, Object> transitionPayload : mapList(stateMachinePayload.get("transitions"))) {
                    String source = stringValue(transitionPayload.get("source"));
                    String target = stringValue(transitionPayload.get("target"));
                    String transitionName = source + "_to_" + target;
                    Element transition = findTransition(region, transitionName);
                    int sourceIndex = states.indexOf(source);
                    int targetIndex = states.indexOf(target);
                    elements.add(diagramElement(
                        document,
                        "EDGE=1;$LLB=;LLT=;LMT=CX=100:CY=16:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LMB=;LRT=;LRB=;IRHS=;ILHS=;Path=;",
                        xmiId(transition),
                        elements.size() + 1,
                        "Mode=3;EOID=" + stateDuids.get(targetIndex) + ";SOID=" + stateDuids.get(sourceIndex) + ";Color=-1;LWidth=0;Hidden=0;"
                    ));
                }
                diagrams.appendChild(createDiagram(
                    document,
                    diagramId(stringValue(blockPayload.get("name")) + "." + stateMachineName),
                    blocksPackageId,
                    localId++,
                    stateMachineName,
                    "Statechart",
                    "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;PackageContents=1;Zoom=100;ShowIcons=1;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=0;",
                    "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;MDGDgm=;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;",
                    "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
                    elements,
                    stateMachineId
                ));
            }
        }
        return localId;
    }

    private int appendBlockDefinitionDiagram(
        Document document,
        Element diagrams,
        Element model,
        List<Map<String, Object>> blocks,
        int localId
    ) {
        Element blocksPackage = findPackagedElement(model, "Blocks");
        String blocksPackageId = xmiId(blocksPackage);
        List<Element> elements = new ArrayList<>();
        List<Map<String, Object>> orderedBlocks = new ArrayList<>(blocks);
        orderedBlocks.sort(Comparator.comparing(block -> stringValue(block.get("name"))));
        for (int index = 0; index < orderedBlocks.size(); index++) {
            String blockName = stringValue(orderedBlocks.get(index).get("name"));
            Element block = findPackagedElement(blocksPackage, blockName);
            int left = 80 + (index % 3) * 180;
            int top = 70 + (index / 3) * 120;
            elements.add(diagramElement(
                document,
                "Left=" + left + ";Top=" + top + ";Right=" + (left + 130) + ";Bottom=" + (top + 70) + ";",
                xmiId(block),
                index + 1,
                "DUID=" + duid(blockName) + ";NSL=0;"
            ));
        }
        elements.add(diagramElement(
            document,
            "Left=10;Top=10;Right=700;Bottom=520;",
            blocksPackageId,
            elements.size() + 1,
            "DUID=" + duid("blocks-package") + ";NSL=1;"
        ));
        diagrams.appendChild(createDiagram(
            document,
            diagramId("blocks"),
            blocksPackageId,
            localId++,
            "Blocks",
            "Logical",
            "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;PackageContents=1;Zoom=100;ShowIcons=1;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=0;",
            "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;MDGDgm=SysML1.4::BlockDefinition;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;",
            "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
            elements,
            null
        ));
        return localId;
    }

    private int appendInternalBlockDiagram(
        Document document,
        Element diagrams,
        Element model,
        List<Map<String, Object>> blocks,
        List<Map<String, Object>> connectors,
        int localId
    ) {
        Map<String, Object> systemBlockPayload = findSystemBlock(blocks);
        if (systemBlockPayload == null) {
            return localId;
        }
        Element blocksPackage = findPackagedElement(model, "Blocks");
        Element systemBlock = findPackagedElement(blocksPackage, stringValue(systemBlockPayload.get("name")));
        String systemBlockId = xmiId(systemBlock);
        List<Element> elements = new ArrayList<>();

        List<Map<String, Object>> parts = mapList(systemBlockPayload.get("parts"));
        for (int index = 0; index < parts.size(); index++) {
            String partName = stringValue(parts.get(index).get("name"));
            Element part = findOwnedAttribute(systemBlock, partName);
            int left = 80 + (index % 3) * 180;
            int top = 80 + (index / 3) * 140;
            elements.add(diagramElement(
                document,
                "Left=" + left + ";Top=" + top + ";Right=" + (left + 140) + ";Bottom=" + (top + 90) + ";",
                xmiId(part),
                index + 1,
                "DUID=" + duid(stringValue(systemBlockPayload.get("name")) + "." + partName) + ";NSL=0;"
            ));
        }
        for (Map<String, Object> connectorPayload : connectors) {
            String connectorName = stringValue(connectorPayload.get("name"));
            Element connector = findOwnedConnector(systemBlock, connectorName);
            if (connector != null) {
                elements.add(diagramElement(
                    document,
                    "EDGE=1;$LLB=;LLT=;LMT=CX=100:CY=16:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LMB=;LRT=;LRB=;IRHS=;ILHS=;Path=;",
                    xmiId(connector),
                    elements.size() + 1,
                    "Color=-1;LWidth=0;Hidden=0;"
                ));
            }
        }
        elements.add(diagramElement(
            document,
            "Left=10;Top=10;Right=760;Bottom=520;",
            systemBlockId,
            elements.size() + 1,
            "DUID=" + duid(stringValue(systemBlockPayload.get("name")) + "-ibd") + ";NSL=1;"
        ));
        diagrams.appendChild(createDiagram(
            document,
            diagramId("ibd." + stringValue(systemBlockPayload.get("name"))),
            systemBlockId,
            localId++,
            stringValue(systemBlockPayload.get("name")) + " Internal",
            "CompositeStructure",
            "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;PackageContents=1;Zoom=100;ShowIcons=1;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=0;",
            "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;MDGDgm=SysML1.4::InternalBlock;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;",
            "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
            elements,
            systemBlockId
        ));
        return localId;
    }

    private void appendRequirementDiagram(
        Document document,
        Element diagrams,
        Element model,
        List<Map<String, Object>> requirements,
        int localId
    ) {
        Element requirementsPackage = findPackagedElement(model, "Requirements");
        String requirementsPackageId = xmiId(requirementsPackage);
        List<Element> elements = new ArrayList<>();
        for (int index = 0; index < requirements.size(); index++) {
            Map<String, Object> requirementPayload = requirements.get(index);
            String requirementName = stringValue(requirementPayload.get("name"));
            Element requirement = findPackagedElement(requirementsPackage, requirementName);
            int left = 120;
            int top = 80 + index * 150;
            int width = Math.max(420, Math.min(900, 140 + stringValue(requirementPayload.get("text")).length() * 4));
            elements.add(diagramElement(
                document,
                "Left=" + left + ";Top=" + top + ";Right=" + (left + width) + ";Bottom=" + (top + 100) + ";",
                xmiId(requirement),
                index + 1,
                "DUID=" + duid(requirementName) + ";NSL=0;"
            ));
        }
        elements.add(diagramElement(
            document,
            "Left=10;Top=10;Right=980;Bottom=720;",
            requirementsPackageId,
            elements.size() + 1,
            "DUID=" + duid("requirements-package") + ";NSL=1;"
        ));
        diagrams.appendChild(createDiagram(
            document,
            diagramId("requirements"),
            requirementsPackageId,
            localId,
            "Requirements",
            "Custom",
            "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;PackageContents=1;Zoom=100;ShowIcons=1;ShowTags=1;HideAtts=1;HideOps=1;HideStereo=0;HideElemStereo=0;",
            "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;MDGDgm=SysML1.4::Requirement;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;",
            "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
            elements,
            null
        ));
    }

    private Element createDiagram(
        Document document,
        String diagramId,
        String packageId,
        int localId,
        String name,
        String diagramType,
        String style1,
        String style2,
        String persistentStyle,
        List<Element> elements,
        String parentId
    ) {
        Element diagram = document.createElement("diagram");
        diagram.setAttributeNS(xmiNs, "xmi:id", diagramId);

        Element model = document.createElement("model");
        model.setAttribute("package", packageId);
        model.setAttribute("localID", String.valueOf(localId));
        model.setAttribute("owner", packageId);
        if (parentId != null && !parentId.isBlank()) {
            model.setAttribute("parent", parentId);
        }
        diagram.appendChild(model);

        Element properties = document.createElement("properties");
        properties.setAttribute("name", name);
        properties.setAttribute("type", diagramType);
        diagram.appendChild(properties);

        Element project = document.createElement("project");
        project.setAttribute("author", "sysml-builder");
        project.setAttribute("version", "1.0");
        diagram.appendChild(project);

        Element style1Element = document.createElement("style1");
        style1Element.setAttribute("value", style1);
        diagram.appendChild(style1Element);

        Element style2Element = document.createElement("style2");
        style2Element.setAttribute("value", style2);
        diagram.appendChild(style2Element);

        Element swimlanes = document.createElement("swimlanes");
        swimlanes.setAttribute(
            "value",
            "locked=false;orientation=0;width=0;inbar=false;names=false;color=-1;bold=false;fcol=0;tcol=-1;ofCol=-1;ufCol=-1;hl=1;ufh=0;hh=0;cls=0;bw=0;hli=0;bro=0;"
        );
        diagram.appendChild(swimlanes);

        Element matrixItems = document.createElement("matrixitems");
        matrixItems.setAttribute("value", "locked=false;matrixactive=false;swimlanesactive=true;kanbanactive=false;width=1;clrLine=0;");
        diagram.appendChild(matrixItems);
        diagram.appendChild(document.createElement("extendedProperties"));

        Element persistentStyleElement = document.createElement("persistentstyle");
        persistentStyleElement.setAttribute("value", persistentStyle);
        diagram.appendChild(persistentStyleElement);
        diagram.appendChild(document.createElement("xrefs"));

        Element elementsContainer = document.createElement("elements");
        for (Element element : elements) {
            elementsContainer.appendChild(element);
        }
        diagram.appendChild(elementsContainer);
        return diagram;
    }

    private Element diagramElement(Document document, String geometry, String subject, int seqNo, String style) {
        Element element = document.createElement("element");
        element.setAttribute("geometry", geometry);
        element.setAttribute("subject", subject);
        element.setAttribute("seqno", String.valueOf(seqNo));
        element.setAttribute("style", style);
        return element;
    }

    private void appendValueTypes(Document document, Element root, Element model, List<String> valueTypes) {
        Element packageElement = findPackagedElement(model, "ValueTypes");
        if (packageElement == null) {
            return;
        }
        for (String valueTypeName : valueTypes) {
            Element dataType = findPackagedElement(packageElement, valueTypeName);
            appendStereotype(document, root, "ValueType", "base_DataType", dataType, Map.of());
        }
    }

    private void appendInterfaceBlocks(Document document, Element root, Element model, List<Map<String, Object>> interfaceBlocks) {
        Element packageElement = findPackagedElement(model, "Interfaces");
        if (packageElement == null) {
            return;
        }
        for (Map<String, Object> interfaceBlockPayload : interfaceBlocks) {
            String name = stringValue(interfaceBlockPayload.get("name"));
            Element interfaceBlock = findPackagedElement(packageElement, name);
            appendStereotype(document, root, "InterfaceBlock", "base_Class", interfaceBlock, Map.of());
            for (Map<String, Object> flowPropertyPayload : mapList(interfaceBlockPayload.get("flow_properties"))) {
                Element property = findOwnedAttribute(interfaceBlock, stringValue(flowPropertyPayload.get("name")));
                appendStereotype(
                    document,
                    root,
                    "FlowProperty",
                    "base_Property",
                    property,
                    Map.of("direction", stringValue(flowPropertyPayload.get("direction")))
                );
            }
        }
    }

    private void appendRequirements(Document document, Element root, Element model, List<Map<String, Object>> requirements) {
        Element packageElement = findPackagedElement(model, "Requirements");
        if (packageElement == null) {
            return;
        }
        for (Map<String, Object> requirementPayload : requirements) {
            String name = stringValue(requirementPayload.get("name"));
            Element requirement = findPackagedElement(packageElement, name);
            String requirementId = stringValue(requirementPayload.get("source_contract"));
            if (requirementId.isBlank()) {
                requirementId = name;
            }
            appendStereotype(
                document,
                root,
                "Requirement",
                "base_Class",
                requirement,
                Map.of(
                    "Id", requirementId,
                    "Text", stringValue(requirementPayload.get("text"))
                )
            );
        }
    }

    private void appendBlocks(Document document, Element root, Element model, List<Map<String, Object>> blocks) {
        Element packageElement = findPackagedElement(model, "Blocks");
        if (packageElement == null) {
            return;
        }
        for (Map<String, Object> blockPayload : blocks) {
            String name = stringValue(blockPayload.get("name"));
            Element block = findPackagedElement(packageElement, name);
            appendStereotype(document, root, "Block", "base_Class", block, Map.of());
            for (Map<String, Object> partPayload : mapList(blockPayload.get("parts"))) {
                Element property = findOwnedAttribute(block, stringValue(partPayload.get("name")));
                appendStereotype(document, root, "PartProperty", "base_Property", property, Map.of());
            }
            for (Map<String, Object> portPayload : mapList(blockPayload.get("ports"))) {
                Element port = findOwnedAttribute(block, stringValue(portPayload.get("name")));
                appendStereotype(document, root, "ProxyPort", "base_Port", port, Map.of());
            }
        }
    }

    private void appendRelationships(Document document, Element root, Element model, List<Map<String, Object>> relationships) {
        Element packageElement = findPackagedElement(model, "Relationships");
        if (packageElement == null) {
            return;
        }
        for (Map<String, Object> relationshipPayload : relationships) {
            String kind = stringValue(relationshipPayload.get("kind"));
            String name = stringValue(relationshipPayload.get("name"));
            Element dependency = findPackagedElement(packageElement, name);
            if ("satisfy".equals(kind)) {
                appendStereotype(document, root, "Satisfy", "base_Dependency", dependency, Map.of());
            } else if ("allocate".equals(kind)) {
                appendStereotype(document, root, "Allocate", "base_Dependency", dependency, Map.of());
            }
        }
    }

    private void appendStereotype(
        Document document,
        Element root,
        String stereotypeName,
        String baseAttribute,
        Element baseElement,
        Map<String, String> extraAttributes
    ) {
        if (baseElement == null) {
            return;
        }
        String baseId = baseElement.getAttributeNS(xmiNs, "id");
        if (baseId.isBlank()) {
            return;
        }
        Element stereotype = document.createElementNS(sysmlNs, "sysml:" + stereotypeName);
        stereotype.setAttributeNS(xmiNs, "xmi:id", stereotypeId(stereotypeName, baseId));
        stereotype.setAttribute(baseAttribute, baseId);
        for (Map.Entry<String, String> entry : extraAttributes.entrySet()) {
            stereotype.setAttribute(entry.getKey(), entry.getValue());
        }
        root.appendChild(stereotype);
    }

    private Element findPackagedElement(Element parent, String name) {
        if (parent == null) {
            return null;
        }
        NodeList children = parent.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element
                && "packagedElement".equals(element.getLocalName())
                && name.equals(element.getAttribute("name"))) {
                return element;
            }
        }
        return null;
    }

    private Element findOwnedAttribute(Element parent, String name) {
        if (parent == null) {
            return null;
        }
        NodeList children = parent.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element
                && "ownedAttribute".equals(element.getLocalName())
                && name.equals(element.getAttribute("name"))) {
                return element;
            }
        }
        return null;
    }

    private Element findOwnedBehavior(Element parent, String name) {
        if (parent == null) {
            return null;
        }
        NodeList children = parent.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element
                && "ownedBehavior".equals(element.getLocalName())
                && name.equals(element.getAttribute("name"))) {
                return element;
            }
        }
        return null;
    }

    private Element findOwnedConnector(Element parent, String name) {
        if (parent == null) {
            return null;
        }
        NodeList children = parent.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element
                && "ownedConnector".equals(element.getLocalName())
                && name.equals(element.getAttribute("name"))) {
                return element;
            }
        }
        return null;
    }

    private Element findFirstChild(Element parent, String localName) {
        if (parent == null) {
            return null;
        }
        NodeList children = parent.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element && localName.equals(element.getLocalName())) {
                return element;
            }
        }
        return null;
    }

    private Element findSubvertex(Element region, String name) {
        if (region == null) {
            return null;
        }
        NodeList children = region.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element
                && "subvertex".equals(element.getLocalName())
                && name.equals(element.getAttribute("name"))) {
                return element;
            }
        }
        return null;
    }

    private Element findTransition(Element region, String name) {
        if (region == null) {
            return null;
        }
        NodeList children = region.getChildNodes();
        for (int index = 0; index < children.getLength(); index++) {
            Node child = children.item(index);
            if (child instanceof Element element
                && "transition".equals(element.getLocalName())
                && name.equals(element.getAttribute("name"))) {
                return element;
            }
        }
        return null;
    }

    private String xmiId(Element element) {
        return element == null ? "" : element.getAttributeNS(xmiNs, "id");
    }

    private String diagramId(String seed) {
        return "_sysmlbuilder_diagram_" + sanitize(seed);
    }

    private String duid(String seed) {
        String sanitized = sanitize(seed).toUpperCase();
        return sanitized.length() > 8 ? sanitized.substring(0, 8) : String.format("%1$-8s", sanitized).replace(' ', '0');
    }

    private String sanitize(String seed) {
        StringBuilder builder = new StringBuilder();
        for (char ch : seed.toCharArray()) {
            if (Character.isLetterOrDigit(ch)) {
                builder.append(ch);
            } else {
                builder.append(Integer.toHexString(ch));
            }
        }
        return builder.toString();
    }

    private Map<String, Object> findSystemBlock(List<Map<String, Object>> blocks) {
        for (Map<String, Object> block : blocks) {
            if (!mapList(block.get("parts")).isEmpty() && stringValue(block.get("name")).endsWith("System")) {
                return block;
            }
        }
        for (Map<String, Object> block : blocks) {
            if (!mapList(block.get("parts")).isEmpty()) {
                return block;
            }
        }
        return null;
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

    private String stringValue(Object value) {
        return value == null ? "" : String.valueOf(value);
    }

    private String stereotypeId(String prefix, String baseId) {
        return "_sysmlbuilder_" + prefix + "_" + baseId;
    }
}
