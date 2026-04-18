package Dont_Panic_Batmobile {
    doc 
    /* The book "Don't Panic - The Absolute Beginners Guide to SysML v2" by Tim Weilkiens and Christian Muggeo 
     * uses the Batmobile as a fictional example. 
     *
     * The Batmobile example in this book was inspired by the legendary lecture Jon Holt gave dressed in a Batman costume.
     *
     * The book provides an overview of SysML v2, so it is a small example with many snippets shown throughout the book. 
     * There is therefore also no sophisticated package structure. All elements are in one package.
     */
    part def Vehicle {
        item driver;
        part engine;
        attribute actualSpeed :> ISQSpaceTime::speed;
    }
    interface def PowerInterface {
        end supplierPort : PowerIP;
        end consumerPort : ~PowerIP;
        ref flow of Power from supplierPort.power to consumerPort.power;
    }
    port def PowerIP {
        out item power : Power;
    }
    item def Power {
        attribute value;
    }
    part def Wheel {
        item boundingBox : ShapeItems::RectangularCuboid [1] :> boundingShapes {
            attribute :>> length :> ISQBase::length = 80 [SI::cm];
            attribute :>> width :> ISQBase::length = 26 [SI::cm];
            attribute :>> height :> ISQBase::length = 80 [SI::cm];
        }
        attribute pressure;
    }
    part def BatmobileEngine {
        perform action rocketBoost { in cmd : EngineCommand = engineControl.cmd; }
        port engineControl {
            in item cmd : EngineCommand;
        }
    }
    item def EngineCommand;
    #system def Batmobile :> Vehicle {
        :>> problemStatement := "As a Hero, Batman needs a cool vehicle.";
        :>> systemIdea := "The Batmobile is a black vehicle...";
        part seat [2];
        part body;
        part wheels [4] : Wheel;
        part frontLeftWheel :> wheels;
        part frontRightWheel :> wheels;
        part rearLeftWheel :> wheels;
        part rearRightWheel :> wheels;
        part battery {
            port powerPort : PowerIP;
            attribute capacity;
        }
        part batmobileEngine : BatmobileEngine :>> engine {
            port enginePort : ~PowerIP;
        }
        interface bat2eng : PowerInterface connect battery.powerPort to batmobileEngine.enginePort;
    }
    part def BatmobileNG :> Batmobile {
        part bulletProofWheels [4] :>> wheels {
            part metalCoating;
        }
    }
    individual item def Batman :> Hero {
        attribute realName = "Jon Holt";
    }
    item def Hero;
    #system occurrence bm1 : Batmobile {
        timeslice batmanDriving {
            item :>> driver : Batman;
            snapshot :>> start {
                attribute :>> battery.capacity = 40000 [SI::'W⋅h'];
            }
            snapshot :>> done {
                attribute :>> battery.capacity = 42 [SI::'W⋅h'];
            }
        }
        then timeslice charging {
            item :>> driver = null;
        }
    }
    action def 'Drive Batmobile' {
        first start;
        then action startBatmobile;
        then action scanEnvironment { out status : StatusKind; }
        then decide ;
        if scanEnvironment.status == StatusKind::safe then 'Switch to standard mode';
        if scanEnvironment.status == StatusKind::alert then 'Switch to alert mode';
        action 'Switch to standard mode';
        then endOfStatusCheck;
        action 'Switch to alert mode';
        then endOfStatusCheck;
        merge endOfStatusCheck;
        then done;
    }
    enum def StatusKind {
        safe;
        alert;
    }
    use case def 'Activate rocket booster' {
        subject bm : Batmobile;
        actor driver : Batman;
        objective {
            doc 
            /* The driver wants to activate 
             * the rocket booster to increase 
             * the speed extremely.
             */
        }
    }
    action def ActivateRocketBooster :> 'Activate rocket booster' {
        first start;
        then action prepareBoost;
        then action activateBoost;
        then done;
    }
    requirement def VehicleMaxSpeed {
        doc 
        /* The actual speed of the vehicle shall 
         * be less or equal than the maximum speed.*/
        subject vehicle : Vehicle;
        stakeholder pm : ProductManagement;
        attribute maxSpeed :> ISQSpaceTime::speed;
        require constraint {
            vehicle.actualSpeed <= maxSpeed
        }
    }
    item def ProductManagement;
    requirement batmobileSpecification {
        requirement <REQ42> batmobileMaxSpeed : VehicleMaxSpeed {
            attribute :>> maxSpeed = 230 [SI::'km/h'];
            subject ;
        }
        requirement <REQ43> batmobileAcceleration;
    }
    #system batmobileDesignV23 : Batmobile {
        satisfy batmobileSpecification by batmobileDesignV23;
    }
    part def System {
        doc 
        /* Represents an engineered system that is a system designed or adapted 
         * to interact with an anticipated operational environment to achieve one or more 
         * intended purposes while complying with applicable constraints.  
         */
        attribute problemStatement : ScalarValues::String {
            doc /* The problem solved by the system. */
        }
        attribute systemIdea : ScalarValues::String {
            doc /* The elevator pitch of how the system solves the problem. */
        }
    }
    part systems [*] : System;
    metadata def <system> SystemDSM :> Metaobjects::SemanticMetadata {
        :>> baseType = systems meta SysML::Systems::Usage;
    }
    part def HeroAssociation;
    concern 'Reduce the number of special parts' {
        doc 
        /* Reduce the number of special parts to reduce the dependency
         * to special suppliers and experts.
         */
        subject ;
        stakeholder heroAss : HeroAssociation;
    }
    viewpoint 'system components' {
        frame 'Reduce the number of special parts' {
            subject ;
        }
        require constraint {
            doc 
            /* A system components view shall show the hierarchical
             * part decomposition of a system, starting with a
             * specified root part.
             */
        }
    }
    view def 'Part list' :> DS_Views::TabularViews::gt {
        satisfy 'system components' {
            subject ;
        }
    }
    view batmobileParts : 'Part list' {
        filter DS_Functions::IsNonStandardLibraryElement();
        expose Dont_Panic_Batmobile::**;
    }
    part def StandardEngine :> BatmobileEngine;
    part def XtremeEngine :> BatmobileEngine;
    part def StandardWheel :> Wheel;
    part def XtremeWheel :> Wheel;
    variation part def EngineChoices :> BatmobileEngine {
        variant part sEngine : StandardEngine;
        variant part xEngine : XtremeEngine;
    }
    variation part def WheelChoices :> Wheel {
        variant part sWheel : StandardWheel;
        variant part xWheel : XtremeWheel;
    }
    part def BatmobileConfigurations :> Batmobile {
        part :>> batmobileEngine : EngineChoices;
        part :>> wheels [4] : WheelChoices;
        assert constraint {
            batmobileEngine == batmobileEngine::xEngine and wheels == wheels.xWheel
        }
    }
    part def XBatmobile :> BatmobileConfigurations {
        part :>> batmobileEngine = batmobileEngine.xEngine;
        part :>> wheels = wheels.xWheel;
    }
    view 'definition and usage' : DS_Views::SymbolicViews::gv;
    view subclassification : DS_Views::SymbolicViews::gv;
    view subsetting : DS_Views::SymbolicViews::gv;
    view redefinition : DS_Views::SymbolicViews::gv;
    view 'structural Modeling' : DS_Views::SymbolicViews::gv;
    view 'default value' : DS_Views::SymbolicViews::gv;
    view 'timeslice modelling' : DS_Views::SymbolicViews::gv;
    view 'behavioral modelling' : DS_Views::SymbolicViews::gv;
    view 'use cases modelling' : DS_Views::SymbolicViews::gv;
    view 'requirements modelling' : DS_Views::SymbolicViews::gv;
}
view index : DS_Views::SymbolicViews::gv;
