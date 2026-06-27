BATCHES = [
    {
        "name": "trl_1_to_3",
        "tree_query": "scientific principles, hypothesis, research problem, literature review, scientific rationale, feasibility, system architecture, core concept validation, lab scale, component validation",
        "pages_hint": None,
        "trl_questions": [
            {"param": "is_scientific_principles_observed",
             "question": "Have the basic scientific principles underlying the concept been observed and reported?"},
            {"param": "is_research_hypothesis_formulated",
             "question": "Has a specific research hypothesis or proposed concept been clearly formulated?"},
            {"param": "is_research_problem_defined",
             "question": "Is the research problem or knowledge gap clearly stated?"},
            {"param": "is_literature_review_conducted",
             "question": "Has a literature review been conducted to explore relevant theories and past findings?"},
            {"param": "has_scientific_rationale",
             "question": "Is there some structured scientific/technical reasoning showing why the idea should work?"},
            {"param": "is_design_solution_identified",
             "question": "Has a clear theoretical or empirical design solution been identified for the technology?"},
            {"param": "are_practical_applications_identified",
             "question": "Have potential practical applications for the system or component been clearly identified?"},
            {"param": "is_feasibility_confirmed_by_analysis",
             "question": "Do analytical or 'paper' studies confirm that the application/product/technology is feasible?"},
            {"param": "are_assumptions_constraints_identified",
             "question": "Are key assumptions, constraints, and dependencies identified?"},
            {"param": "is_system_architecture_defined",
             "question": "Has the system architecture been defined in terms of major functions to be performed?"},
            {"param": "experiment_tests_core_concept",
             "question": "Are experiments or simulations designed specifically to test the core functionality?"},
            {"param": "is_core_concept_validated",
             "question": "Has the core concept or hypothesis been experimentally validated (like small experiment, tiny prototype, bench test, etc.)?"},
            {"param": "are_critical_components_lab_validated",
             "question": "Have the critical individual components been tested and validated at a laboratory scale?"},
            {"param": "are_results_compared_to_baselines",
             "question": "Are results compared with baselines, prior methods, or expected behavior?"},
            {"param": "are_limitations_discussed",
             "question": "Are limitations, assumptions, or failure cases discussed?"},
    
        ]
    },

    {
        "name": "trl_4_to_6",
        "tree_query": "breadboard, integrated system lab validation, failure mode, risk analysis, relevant environment, realistic conditions, high-fidelity components, interface testing, operational characteristics, high-fidelity prototype, engineering feasibility",
        "pages_hint": None,
        "trl_questions": [
            {"param": "is_breadboard_system_assembled",
             "question": "Have available components been assembled into a system breadboard or 'ad-hoc' integrated system?"},
            {"param": "is_integrated_system_lab_validated",
             "question": "Does laboratory experiments shown that these integrated components successfully work together and/or demonstrate expected functionality?"},
            {"param": "is_low_fidelity_integration_completed",
             "question": "Has low-fidelity 'system' integration and engineering been successfully completed in a lab environment?"},
            {"param": "is_preliminary_risk_analysis_performed",
             "question": "Has a preliminary Failure Mode and Effects Analysis (FMEA) or structured risk analysis been performed?"},
            {"param": "is_system_validated_in_relevant_environment",
             "question": "Has the integrated system been successfully validated in a relevant/realistic or simulated environment outside of a basic lab setting?"},
            {"param": "do_subsystems_function_under_realistic_conditions",
             "question": "Do integrated components/subsystems function together correctly under realistic conditions?"},
            {"param": "are_components_high_fidelity",
             "question": "Are the components high-fidelity versions of the final design?"},
            {"param": "are_subsystem_interfaces_tested",
             "question": "Have internal subsystem interfaces been defined and tested?"},
            {"param": "are_operational_characteristics_measured",
             "question": "Are reliability, consistency, operational limitations, constraints, performance degradations or repeatability measurements identified under realistic conditions?"},
            {"param": "is_environment_gap_understood",
             "question": "Is there a clear understanding of how the simulated testing environment differs from the expected operational environment?"},
            {"param": "is_high_fidelity_prototype_demonstrated",
             "question": "Has an engineering or pilot-scale high fidelity representative model/prototype been successfully demonstrated in a relevant/realistic environment?"},
            {"param": "is_engineering_feasibility_demonstrated",
             "question": "Has the engineering feasibility of the system been fully demonstrated?"},
            {"param": "is_end_to_end_workflow_operational",
             "question": "Are all critical system functionalities operating together in an end-to-end integrated workflow?"},
            {"param": "are_interfaces_operationally_realistic",
             "question": "Are the interfaces between the components/subsystems realistic for the final operational environment?"},
            {"param": "is_operating_environment_defined",
             "question": "Is the eventual operating environment for the system fully known?"},
            {"param": "are_operational_risks_documented",
             "question": "Have deployment, engineering, integration, and operational risks been formally analyzed and documented?"},
            
        ]
    },

    {
        "name": "trl_7_to_9",
        "tree_query": "operational environment, deployment risks, full-scale prototype, real-world conditions, steady operation, operational metrics, field feedback, formal qualification, regulatory certifications, production process, configuration control, lifecycle management",
        "pages_hint": None,
        "trl_questions": [
            {"param": "is_full_scale_prototype_demonstrated",
             "question": "Has a fully integrated, full-scale prototype (with ready form, fit, and function) been demonstrated in an actual operational environment?"},
            {"param": "is_system_tested_in_real_world_conditions",
             "question": "Is the system tested using real-world workflows, users, data, or operating conditions?"},
            {"param": "is_system_stable_in_operation",
             "question": "Does system sustain stable operation in actual operational environment?"},
            {"param": "are_operational_metrics_reported",
             "question": "Are operational performance metrics (e.g., latency, throughput, robustness, uptime, accuracy) reported?"},
            {"param": "are_operational_edge_cases_evaluated",
             "question": "Are real operational edge cases, disturbances, or failure scenarios evaluated?"},
            {"param": "is_field_feedback_documented",
             "question": "Are operational observations, user feedback, or field-performance findings documented?"},
            {"param": "is_system_formally_qualified",
             "question": "Has the final system been fully integrated and qualified through formal test and evaluation (final real-world operational environment) against its design specifications?"},
            {"param": "are_regulatory_approvals_obtained",
             "question": "Are all required regulatory certifications, safety compliances, or industry benchmarks fully approved?"},
            {"param": "is_production_process_used",
             "question": "Was the final system built/deployed using the actual production-line manufacturing or final software release processes?"},
            {"param": "is_configuration_control_established",
             "question": "Is the system design strictly under configuration control (e.g., frozen baseline, formal change management process)?"},
            {"param": "is_operational_test_completed",
             "question": "Has Operational Test and Evaluation (OT&E) been successfully completed?"},
            {"param": "are_long_term_test_reports_completed",
             "question": "Are long-duration reliability, maintainability, availability, or stability test reports completed?"},
            {"param": "is_operational_documentation_finalized",
             "question": "Are user manuals, maintenance documentation, and operator training materials fully finalized?"},
            {"param": "are_qualification_defects_resolved",
             "question": "Have all identified defects from qualification testing been resolved, or formally accepted as low-risk deviations?"},
            {"param": "is_system_proven_in_operation",
             "question": "Has the actual system been successfully deployed and proven through sustained, routine real-world operations or mission success?"},
            {"param": "is_performance_validated_across_conditions",
             "question": "Has the system demonstrated stable performance under the full range of actual operational conditions and unexpected environments?"},
            {"param": "is_final_design_frozen",
             "question": "Is the final design completely frozen, with any future changes limited strictly to maintenance or minor product improvements?"},
            {"param": "are_lifecycle_processes_operational",
             "question": "Are maintenance, monitoring, field support, and supply chain/lifecycle management processes fully operational?"},
            {"param": "are_quality_control_processes_established",
             "question": "Are manufacturing and deployment processes controlled to standard quality levels (e.g., Six Sigma, ISO) to ensure repeatable, defect-free production?"},
            {"param": "is_long_term_adoption_demonstrated",
             "question": "Is there clear evidence of long-term adoption, scaling, or routine user utilization?"},
            {"param": "are_post_deployment_metrics_tracked",
             "question": "Are post-deployment operational metrics (e.g., actual field reliability data, total cost of ownership) being actively tracked and reviewed?"},
        ]
    }]


def build_prompt(
    paper_text: str = "",
    trl_questions: list[dict] = None,
) -> str:

    if trl_questions is None:
        # Gather all questions from all batches
        trl_questions = [q for batch in BATCHES for q in batch["trl_questions"]]

    trl_specific_prompt = ""
    if trl_questions:
        trl_list = "\n".join(
            f'  - param: "{q["param"]}" | question: "{q["question"]}"'
            for q in trl_questions
        )
        trl_specific_prompt = f"""You are an expert research analyst and pioneer in evidence based assessment of research papers.
Your task is to extract general paper metadata and answer specific Technology Readiness Level (TRL) questions based on the paper text provided below.

### GENERAL METADATA EXTRACTION RULES ###
Extract the following general metadata fields:
1. "research_title": The actual title of the paper printed inside the research paper (NOT the filename).
2. "authors": An array/list of strings for each author (e.g., ["John Doe", "Jane Smith"]). Do not include affiliations in this array.
3. "abstract": The text abstract of the paper.
4. "published_year": The year the paper was published as an integer (e.g., 2024, or null if not found).
5. "venue": The publishing venue or platform where the paper is published (e.g., "arXiv", "IEEE", "ACM", "Springer", "Elsevier", a specific journal/conference name, etc., or null if not found).
6. "doi": The Digital Object Identifier (DOI) of the paper, if mentioned (e.g., "10.1109/5.771073", or null if not found).
7. "language": The language the paper is written in (e.g., "English", or null if not found).
8. "country_of_origin": The country of origin of the paper, based on authors' affiliations or publication details (or null if not found).
9. "paper_type": A string categorizing the paper. Must be one of: "survey", "empirical", "theoretical", "benchmark", "thesis", or null if not found.

### TRL SPECIFIC QUESTIONS TO ANSWER ###
{trl_list}

Rules for trl_specific:
- Return a dict mapping each param to a nested JSON object with:
    - "decision": "yes" or "no" (strictly)
    - "evidence": A JSON object with one or more keys (evd_1, evd_2, etc.) where each key maps to an object containing:
        - "page_number": integer
        - "section_of_paper": string, title of the section
        - "evidence_text": string, the exact text from the paper that serves as evidence.
    - "justification": detailed justification/rationale for the decision (yes/no) 
    - "confidence": percentage 0 to 100% (use 100% if strongly confident, 71% to 100% if satisfactorily passed/decently confident, else below 70%)

### OUTPUT FORMAT ###
Return ONLY a valid JSON structure matching the schema below. Do not wrap it in markdown code blocks in your raw API response (if requested by the config, the client will parse it), do not output any extra text or conversational filler:
{{
  "metadata": {{
    "research_title": "<string or null>",
    "authors": ["<string>", "..."],
    "abstract": "<string or null>",
    "published_year": <integer or null>,
    "venue": "<string or null>",
    "doi": "<string or null>",
    "language": "<string or null>",
    "country_of_origin": "<string or null>",
    "paper_type": "<'survey' | 'empirical' | 'theoretical' | 'benchmark' | 'thesis' | null>"
  }},
  "trl_specific": {{
    "<param_name>": {{
      "decision": "yes/no",
      "evidence": {{
        "evd_1": {{
          "page_number": <integer>,
          "section_of_paper": "<string>",
          "evidence_text": "<string>"
        }}
      }},
      "justification": "<detailed justification>",
      "confidence": "<0-100%>"
    }},
    "...": "..."
  }}
}}

### PAPER TEXT ###
{paper_text}
"""

    return trl_specific_prompt


if __name__ == "__main__":
    prompt = build_prompt("paper data")
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
