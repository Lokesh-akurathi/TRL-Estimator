trl_fields={
  "TRL_1": {
    "Hard":{
      "questions": {
        "is_scientific_principles_observed": "Have the basic scientific principles underlying the concept been observed and reported?",
        "is_research_hypothesis_formulated": "Has a specific research hypothesis or proposed concept been clearly formulated?",
        "is_research_problem_defined": "Is the research problem or knowledge gap clearly stated?"
      }
    },
    "Soft":{
      "questions": {
        "is_literature_review_conducted": "Has a literature review been conducted to explore relevant theories and past findings?",
        "has_scientific_rationale": "Is there some structured scientific/technical reasoning showing why the idea should work?"
      }
    }
  },
  "TRL_2": {
    "Hard": {
      "questions": {
        "is_design_solution_identified": "Has a clear theoretical or empirical design solution been identified for the technology?",
        "are_practical_applications_identified": "Have potential practical applications for the system or component been clearly identified?",
        "is_feasibility_confirmed_by_analysis": "Do analytical or \"paper\" studies confirm that the application/product/technology is feasible?"
      }
    },
    "Soft": {
      "questions": {
        "are_assumptions_constraints_identified": "Are key assumptions, constraints, and dependencies identified?",
        "is_system_architecture_defined": "Has the system architecture been defined in terms of major functions to be performed?"
      }
    }
  },
  "TRL_3": {
    "Hard": {
      "questions": {
        "experiment_tests_core_concept": "Are experiments or simulations designed specifically to test the core functionality?",
        "is_core_concept_validated": "Has the core concept or hypothesis been experimentally validated (like small experiment, tiny prototype, bench test, etc..)?",
        "are_critical_components_lab_validated": "Have the critical individual components been tested and validated at a laboratory scale?"
      }
    },
    "Soft": {
      "questions": {
        "are_results_compared_to_baselines": "Are results compared with baselines, prior methods, or expected behavior?",
        "are_limitations_discussed": "Are limitations, assumptions, or failure cases discussed?"
      }
    }
  },
  "TRL_4": {
    "Hard": {
      "questions": {
        "is_breadboard_system_assembled": "Have available components been assembled into a system breadboard or \"ad-hoc\" integrated system?",
        "is_integrated_system_lab_validated": "Does laboratory experiments shown that these integrated components successfully work together and/or demonstrate expected functionality?",
        "is_low_fidelity_integration_completed": "Has low-fidelity \"system\" integration and engineering been successfully completed in a lab environment?"
      }
    },
    "Soft": {
      "questions": {
        "is_preliminary_risk_analysis_performed": "Has a preliminary Failure Mode and Effects Analysis (FMEA) or structured risk analysis been performed?"
      }
    }
  },
  "TRL_5": {
    "Hard": {
      "questions": {
        "is_system_validated_in_relevant_environment": "Has the integrated system been successfully validated in a relevant/realistic or simulated environment outside of a basic lab setting?",
        "do_subsystems_function_under_realistic_conditions": "Do integrated components/subsystems function together correctly under realistic conditions?",
        "are_components_high_fidelity": "Are the components high-fidelity versions of the final design?",
        "are_subsystem_interfaces_tested": "Have internal subsystem interfaces been defined and tested?"
      }
    },
    "Soft": {
      "questions": {
        "are_operational_characteristics_measured": "Are reliability, consistency, operational limitations, constraints, performance degradations or repeatability measurements identified under realistic conditions?",
        "is_environment_gap_understood": "Is there a clear understanding of how the simulated testing environment differs from the expected operational environment?"
      }
    }
  },
  "TRL_6": {
    "Hard": {
      "questions": {
        "is_high_fidelity_prototype_demonstrated": "Has an engineering or pilot-scale high fidelity representative model/prototype been successfully demonstrated in a relevant/realistic environment?",
        "is_engineering_feasibility_demonstrated": "Has the engineering feasibility of the system been fully demonstrated?",
        "is_end_to_end_workflow_operational": "Are all critical system functionalities operating together in an end-to-end integrated workflow?",
        "are_interfaces_operationally_realistic": "Are the interfaces between the components/subsystems realistic for the final operational environment?"
      }
    },
    "Soft": {
      "questions": {
        "is_operating_environment_defined": "Is the eventual operating environment for the system fully known?",
        "are_operational_risks_documented": "Have deployment, engineering, integration, and operational risks been formally analyzed and documented?"
      }
    }
  },
  "TRL_7": {
    "Hard": {
      "questions": {
        "is_full_scale_prototype_demonstrated": "Has a fully integrated, full-scale prototype (with ready form, fit, and function) been demonstrated in an actual operational environment?",
        "is_system_tested_in_real_world_conditions": "Is the system tested using real-world workflows, users, data, or operating conditions?",
        "is_system_stable_in_operation": "Does system sustain stable operation in actual operational environment?",
        "are_operational_metrics_reported": "Are operational performance metrics (e.g., latency, throughput, robustness, uptime, accuracy) reported?"
      }
    },
    "Soft": {
      "questions": {
        "are_operational_edge_cases_evaluated": "Are real operational edge cases, disturbances, or failure scenarios evaluated?",
        "is_field_feedback_documented": "Are operational observations, user feedback, or field-performance findings documented?"
      }
    }
  },
  "TRL_8": {
    "Hard": {
      "questions": {
        "is_system_formally_qualified": "Has the final system been fully integrated and qualified through formal test and evaluation (final real-world operational environment) against its design specifications?",
        "are_regulatory_approvals_obtained": "Are all required regulatory certifications, safety compliances, or industry benchmarks fully approved?",
        "is_production_process_used": "Was the final system built/deployed using the actual production-line manufacturing or final software release processes?",
        "is_configuration_control_established": "Is the system design strictly under configuration control (e.g., frozen baseline, formal change management process)?",
        "is_operational_test_completed": "Has Operational Test and Evaluation (OT&E) been successfully completed?"
      }
    },
    "Soft": {
      "questions": {
        "are_long_term_test_reports_completed": "Are long-duration reliability, maintainability, availability, or stability test reports completed?",
        "is_operational_documentation_finalized": "Are user manuals, maintenance documentation, and operator training materials fully finalized?",
        "are_qualification_defects_resolved": "Have all identified defects from qualification testing been resolved, or formally accepted as low-risk deviations?"
      }
    }
  },
  "TRL_9": {
    "Hard": {
      "questions": {
        "is_system_proven_in_operation": "Has the actual system been successfully deployed and proven through sustained, routine real-world operations or mission success?",
        "is_performance_validated_across_conditions": "Has the system demonstrated stable performance under the full range of actual operational conditions and unexpected environments?",
        "is_final_design_frozen": "Is the final design completely frozen, with any future changes limited strictly to maintenance or minor product improvements?",
        "are_lifecycle_processes_operational": "Are maintenance, monitoring, field support, and supply chain/lifecycle management processes fully operational?",
        "are_quality_control_processes_established": "Are manufacturing and deployment processes controlled to standard quality levels (e.g., Six Sigma, ISO) to ensure repeatable, defect-free production?"
      }
    },
    "Soft": {
      "questions": {
        "is_long_term_adoption_demonstrated": "Is there clear evidence of long-term adoption, scaling, or routine user utilization?",
        "are_post_deployment_metrics_tracked": "Are post-deployment operational metrics (e.g., actual field reliability data, total cost of ownership) being actively tracked and reviewed?"
      }
    }
  }
}