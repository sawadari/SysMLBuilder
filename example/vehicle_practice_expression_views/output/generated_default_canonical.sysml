package VehiclePracticeExpressionViews {
    package RequirementsModel {
        private import DS_Views::*;

        requirement def MassRequirement {
            doc /* The actual mass shall be less than or equal to the limit. */
            attribute massActual : ScalarValues::Real;
            attribute massLimit  : ScalarValues::Real;
            require constraint { massActual <= massLimit }
        }

        requirement vehicleSpecification {
            requirement vehicleMass : MassRequirement {
                attribute :>> massActual = 1450;
                attribute :>> massLimit  = 1800;
            }

            requirement engineMass : MassRequirement {
                attribute :>> massActual = 220;
                attribute :>> massLimit  = 250;
            }
        }

        // If your Cameo build resolves only RequirementTreeView, replace the type name below.
        view 'Requirements Tree' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
            expose VehiclePracticeExpressionViews::RequirementsModel::**;
        }
    }

    package StructureModel {
        private import DS_Views::*;

        item def DriveTorque {
            attribute value : ScalarValues::Real;
        }

        port def DrivePwrPort {
            out item torque : DriveTorque;
        }

        part def Engine {
            port drivePwrPort : DrivePwrPort;
        }

        part def Transmission {
            port clutchPort : ~DrivePwrPort;
        }

        interface def EngineToTransmissionInterface {
            end enginePort       : DrivePwrPort;
            end transmissionPort : ~DrivePwrPort;

            flow of DriveTorque from enginePort.torque to transmissionPort.torque;
        }

        part def Vehicle {
            part engine       : Engine;
            part transmission : Transmission;

            interface engineToTransmission : EngineToTransmissionInterface
            connect engine::drivePwrPort to transmission::clutchPort;
        }

        part vehicle1 : Vehicle;

        view 'Parts Tree' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
            expose VehiclePracticeExpressionViews::StructureModel::**;
        }

        view 'Parts Nested' : DS_Views::SymbolicViewsByExpression::PartsNestedView {
            expose VehiclePracticeExpressionViews::StructureModel::**;
        }

        view 'Parts & Ports Nested' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
            expose VehiclePracticeExpressionViews::StructureModel::**;
        }

      view 'System Interconnection' : DS_Views::SymbolicViews::iv {
          expose VehiclePracticeExpressionViews::StructureModel::**;
      }
    }

    package BehaviorActionModel {
        private import DS_Views::*;

        item def Command;
        item def Torque;

        action def GenerateTorque {
            in item cmd : Command;
            out item torque : Torque;
        }

        action def TransferTorque {
            in item inTorque : Torque;
            out item outTorque : Torque;
        }

        action providePower {
            action generateTorque : GenerateTorque;
            action transferTorque : TransferTorque;

            flow of Torque from generateTorque.torque to transferTorque.inTorque;
        }

        view 'Actions Nested' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
            expose VehiclePracticeExpressionViews::BehaviorActionModel::**;
        }

        view 'Actions Tree' : DS_Views::SymbolicViewsByExpression::ActionsTreeView {
            expose VehiclePracticeExpressionViews::BehaviorActionModel::**;
        }

      view 'Action Flow View' : DS_Views::SymbolicViews::afv {
          expose VehiclePracticeExpressionViews::BehaviorActionModel::**;
      }
    }

    package BehaviorStateModel {
        private import DS_Views::*;

        attribute def StartSignal;
        attribute def OffSignal;

        part def Controller {
            exhibit state controllerStates parallel {
                state operatingStates {
                    entry action initial;

                    state off;
                    state on;

                    transition initial then off;

                    transition off_to_on
                        first off
                        accept StartSignal
                        then on;

                    transition on_to_off
                        first on
                        accept OffSignal
                        then off;
                }
            }
        }

        part controller1 : Controller;

        view 'States Nested' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
            expose VehiclePracticeExpressionViews::BehaviorStateModel::**;
        }

      view 'State Transition View' : DS_Views::SymbolicViews::stv {
          expose VehiclePracticeExpressionViews::BehaviorStateModel::**;
      }
    }
}
