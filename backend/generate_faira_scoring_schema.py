#!/usr/bin/env python3
"""
Comprehensive FAIRA Scoring Schema Generator
Builds the complete scoring configuration from scratch based on user specifications.
"""
import json
from pathlib import Path

def generate_complete_scoring_schema():
    """
    Generate the complete FAIRA scoring schema with all configured questions.
    This includes A1, A2, A3, A4.1, and A4.2.
    """
    
    schema = {
        "_meta": {
            "version": "1.0",
            "description": "FAIRA Risk Assessment Scoring Configuration",
            "formula": "Raw Risk Score = (Total Impact × Total Likelihood) / Control Effectiveness",
            "special_modifiers": {
                "AutonomyFactor": "Computed from A1.6 (autonomy level)",
                "DataQualityFactor": "Computed from A2.5 (data quality ratings)",
                "ExpertiseFactor": "Computed from A3.2 (user expertise levels)"
            }
        },
        "questions": {}
    }
    
    # ============================================================================
    # SECTION A1: AI Solution Fundamentals
    # ============================================================================
    
    # A1.1 - Primary Function → Impact
    schema["questions"]["A1_1"] = {
        "id": "A1_1",
        "text": "What is the primary function of the AI system?",
        "type": "multiselect",
        "domains": ["Accountability", "Transparency"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Automate routine tasks": {"Impact": 1},
                "Support human decision-making": {"Impact": 2},
                "Make autonomous decisions": {"Impact": 3},
                "Predict outcomes": {"Impact": 2},
                "Generate content": {"Impact": 1},
                "Classify or categorize data": {"Impact": 1},
                "Detect anomalies or patterns": {"Impact": 2},
                "Other": {"Impact": 1}
            }
        }
    }
    
    # A1.2 - AI System Version → No scoring
    schema["questions"]["A1_2"] = {
        "id": "A1_2",
        "text": "What version is the AI system currently at?",
        "type": "text",
        "domains": ["Accountability"],
        "scoring": None
    }
    
    # A1.3 - AI Features → Impact
    schema["questions"]["A1_3"] = {
        "id": "A1_3",
        "text": "Which AI features or capabilities does the system include?",
        "type": "multiselect",
        "domains": ["Accountability", "Transparency"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Natural language processing": {"Impact": 1},
                "Computer vision": {"Impact": 1},
                "Recommendation engine": {"Impact": 2},
                "Predictive modeling": {"Impact": 2},
                "Anomaly detection": {"Impact": 2},
                "Speech recognition": {"Impact": 1},
                "Automated content generation": {"Impact": 1},
                "Optimization algorithms": {"Impact": 2},
                "Reinforcement learning": {"Impact": 3},
                "Other": {"Impact": 1}
            }
        }
    }
    
    # A1.4 - Decisions Addressed → Impact
    schema["questions"]["A1_4"] = {
        "id": "A1_4",
        "text": "What types of decisions or problems does the AI system address?",
        "type": "multiselect",
        "domains": ["Accountability", "Fairness"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Operational efficiency": {"Impact": 1},
                "Resource allocation": {"Impact": 2},
                "Risk assessment": {"Impact": 3},
                "Customer interactions": {"Impact": 2},
                "Compliance and regulatory": {"Impact": 3},
                "Safety monitoring": {"Impact": 3},
                "Quality control": {"Impact": 2},
                "Strategic planning": {"Impact": 2},
                "Personnel management": {"Impact": 3}
            }
        }
    }
    
    # A1.5 - Tangible Benefits → Impact (Negative - Risk Reduction)
    schema["questions"]["A1_5"] = {
        "id": "A1_5",
        "text": "What tangible benefits does the AI system provide?",
        "type": "multiselect",
        "domains": ["Accountability"],
        "scoring": {
            "target_metric": "Impact",
            "modifier_type": "negative",
            "options": {
                "Cost reduction": {"Impact": -1},
                "Time savings": {"Impact": -1},
                "Improved accuracy": {"Impact": -2},
                "Enhanced user experience": {"Impact": -1},
                "Scalability": {"Impact": -1},
                "Better decision-making": {"Impact": -2},
                "Risk mitigation": {"Impact": -2},
                "Compliance support": {"Impact": -2}
            }
        }
    }
    
    # A1.6 - Autonomy Level → Likelihood (via AutonomyFactor)
    schema["questions"]["A1_6"] = {
        "id": "A1_6",
        "text": "Does the system convert its outputs directly into actions without human intervention?",
        "type": "yes_no",
        "domains": ["Accountability", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Likelihood",
            "special_computation": "AutonomyFactor",
            "options": {
                "No": {"base": 1.0},
                "Yes": {
                    "base": 2.0,
                    "sub_question": "A1_6_actions",
                    "actions": {
                        "Notifications only": {"multiplier": 1.0},
                        "Data updates": {"multiplier": 1.2},
                        "Workflow triggers": {"multiplier": 1.3},
                        "Financial transactions": {"multiplier": 1.8},
                        "Access control changes": {"multiplier": 1.5},
                        "Content publication": {"multiplier": 1.4},
                        "Equipment control": {"multiplier": 1.9},
                        "Other": {"multiplier": 1.1}
                    }
                }
            },
            "notes": "AutonomyFactor = base × max(action_multipliers). This modifies Total Likelihood in final calculation."
        }
    }
    
    # A1.7 - AI Model Type → Impact
    schema["questions"]["A1_7"] = {
        "id": "A1_7",
        "text": "What type(s) of AI model or algorithm does the system use?",
        "type": "multiselect",
        "domains": ["Transparency", "Accountability"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Rule-based system": {"Impact": 1},
                "Linear/logistic regression": {"Impact": 1},
                "Decision trees": {"Impact": 1},
                "Random forest": {"Impact": 1},
                "Neural networks": {"Impact": 2},
                "Deep learning": {"Impact": 2},
                "Ensemble methods": {"Impact": 2},
                "Generative AI": {"Impact": 3},
                "Reinforcement learning": {"Impact": 3},
                "Other": {"Impact": 1}
            }
        }
    }
    
    # A1.8 - AI Source → Impact
    schema["questions"]["A1_8"] = {
        "id": "A1_8",
        "text": "Where did the AI system or model originate?",
        "type": "multiselect",
        "domains": ["Accountability", "Transparency"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Developed in-house": {"Impact": 2},
                "Third-party vendor": {"Impact": 3},
                "Open-source model": {"Impact": 2},
                "Cloud-based service": {"Impact": 2},
                "Pre-trained model (customized)": {"Impact": 2},
                "Pre-trained model (used as-is)": {"Impact": 3}
            }
        }
    }
    
    # A1.9 - Integration → Likelihood
    schema["questions"]["A1_9"] = {
        "id": "A1_9",
        "text": "How is the AI system integrated into your operations?",
        "type": "multiselect",
        "domains": ["Reliability and Safety"],
        "scoring": {
            "target_metric": "Likelihood",
            "options": {
                "Standalone tool": {"Likelihood": 1},
                "Embedded in existing software": {"Likelihood": 2},
                "Part of a broader system": {"Likelihood": 2},
                "API or cloud service": {"Likelihood": 2},
                "Mobile or edge deployment": {"Likelihood": 3},
                "Real-time system": {"Likelihood": 3}
            }
        }
    }
    
    # ============================================================================
    # SECTION A2: Data and Inputs
    # ============================================================================
    
    # A2.1 - Data Tracking → Control Effectiveness (Negative - improves control)
    schema["questions"]["A2_1"] = {
        "id": "A2_1",
        "text": "How are data sources and quality tracked?",
        "type": "multiselect",
        "domains": ["Data Integrity", "Transparency"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "We maintain a data catalog": {"Control_Effectiveness": -2},
                "We track data lineage": {"Control_Effectiveness": -2},
                "We monitor data quality metrics": {"Control_Effectiveness": -3},
                "We version control datasets": {"Control_Effectiveness": -1},
                "We document data transformations": {"Control_Effectiveness": -2},
                "No formal tracking": {"Control_Effectiveness": 0}
            }
        }
    }
    
    # A2.2 - Environmental Data → Impact
    schema["questions"]["A2_2"] = {
        "id": "A2_2",
        "text": "What environmental, external, or real-time data does the system rely on?",
        "type": "text",
        "domains": ["Data Integrity", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Impact",
            "logic": "Text analysis required - not scored automatically"
        }
    }
    
    # A2.3 - Data Safeguards → Control Effectiveness (Negative - improves control)
    schema["questions"]["A2_3"] = {
        "id": "A2_3",
        "text": "What safeguards exist to ensure data quality and integrity?",
        "type": "multiselect",
        "domains": ["Data Integrity", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "Automated validation rules": {"Control_Effectiveness": -2},
                "Manual review processes": {"Control_Effectiveness": -1},
                "Data cleansing pipelines": {"Control_Effectiveness": -2},
                "Anomaly detection": {"Control_Effectiveness": -3},
                "Access controls": {"Control_Effectiveness": -1},
                "Regular audits": {"Control_Effectiveness": -2},
                "No safeguards": {"Control_Effectiveness": 0}
            }
        }
    }
    
    # A2.4 - Data Types → Impact
    schema["questions"]["A2_4"] = {
        "id": "A2_4",
        "text": "What types of data does the system process?",
        "type": "multiselect",
        "domains": ["Privacy", "Data Integrity"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Personal information": {"Impact": 3},
                "Financial data": {"Impact": 3},
                "Health information": {"Impact": 3},
                "Operational metrics": {"Impact": 1},
                "Transactional data": {"Impact": 2},
                "Behavioral data": {"Impact": 2},
                "Environmental sensors": {"Impact": 1},
                "Public data": {"Impact": 1},
                "Other": {"Impact": 1}
            }
        }
    }
    
    # A2.5 - Data Quality → Likelihood (via DataQualityFactor)
    schema["questions"]["A2_5"] = {
        "id": "A2_5",
        "text": "Rate the quality of input data on the following dimensions (1-5 scale)",
        "type": "rating_multi",
        "domains": ["Data Integrity", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Likelihood",
            "special_computation": "DataQualityFactor",
            "dimensions": {
                "accuracy": {"field": "A2_5_accuracy"},
                "completeness": {"field": "A2_5_completeness"},
                "reliability": {"field": "A2_5_reliability"},
                "relevance": {"field": "A2_5_relevance"},
                "timeliness": {"field": "A2_5_timeliness"}
            },
            "formula": "DataQualityFactor = 6 - (average of 5 ratings)",
            "notes": "Lower quality (rating=1) increases risk. Higher quality (rating=5) reduces risk. Factor ranges from 1.0 (perfect quality) to 5.0 (very poor quality)."
        }
    }
    
    # A2.6 - Business Impact Level (BIL) → Impact
    schema["questions"]["A2_6"] = {
        "id": "A2_6",
        "text": "What is the Business Impact Level (BIL) of the input data?",
        "type": "single_select",
        "domains": ["Privacy", "Security"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "BIL-0 (Public)": {"Impact": 1},
                "BIL-1 (Low)": {"Impact": 2},
                "BIL-2 (Medium)": {"Impact": 3},
                "BIL-3 (High)": {"Impact": 4},
                "BIL-4 (Critical)": {"Impact": 5}
            }
        }
    }
    
    # A2.7 - Regulated Data → Impact
    schema["questions"]["A2_7"] = {
        "id": "A2_7",
        "text": "Does the system process regulated or sensitive data?",
        "type": "yes_no",
        "domains": ["Privacy", "Compliance"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "No": {"Impact": 0},
                "Yes": {"Impact": 3}
            }
        }
    }
    
    # A2.8 - User Inputs Required → Likelihood
    schema["questions"]["A2_8"] = {
        "id": "A2_8",
        "text": "Are user inputs required for the system to function?",
        "type": "yes_no",
        "domains": ["Data Integrity", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Likelihood",
            "options": {
                "No": {"Likelihood": 0},
                "Yes": {"Likelihood": 2}
            }
        }
    }
    
    # ============================================================================
    # SECTION A3: Human Interface and Impact
    # ============================================================================
    
    # A3.1 - Interface Types → Likelihood
    schema["questions"]["A3_1"] = {
        "id": "A3_1",
        "text": "What types of human-AI interfaces does the system use?",
        "type": "multiselect",
        "domains": ["Explainability", "Accountability"],
        "scoring": {
            "target_metric": "Likelihood",
            "options": {
                "Dashboard or visualization": {"Likelihood": 1},
                "Recommendation system": {"Likelihood": 2},
                "Decision support interface": {"Likelihood": 2},
                "Automated alerts": {"Likelihood": 2},
                "Chatbot or conversational AI": {"Likelihood": 2},
                "Direct system integration (no user interface)": {"Likelihood": 3},
                "Other": {"Likelihood": 1}
            }
        }
    }
    
    # A3.2 - User Expertise → Likelihood (via ExpertiseFactor)
    schema["questions"]["A3_2"] = {
        "id": "A3_2",
        "text": "Rate the typical expertise of users interacting with the system (1-5 scale)",
        "type": "rating_multi",
        "domains": ["Accountability", "Explainability"],
        "scoring": {
            "target_metric": "Likelihood",
            "special_computation": "ExpertiseFactor",
            "dimensions": {
                "technical": {"field": "A3_2_technical"},
                "domain": {"field": "A3_2_domain"},
                "ai_literacy": {"field": "A3_2_ai_literacy"}
            },
            "formula": "ExpertiseFactor = 6 - (average of 3 ratings)",
            "notes": "Lower expertise increases likelihood of misuse or misinterpretation. Factor ranges from 1.0 (expert users) to 5.0 (novice users)."
        }
    }
    
    # A3.3 - Impacted Groups → Impact (Group-based with severity)
    schema["questions"]["A3_3"] = {
        "id": "A3_3",
        "text": "Which groups are impacted by the system's decisions?",
        "type": "multiselect",
        "domains": ["Fairness", "Accountability"],
        "scoring": {
            "target_metric": "Impact",
            "groups": {
                "Staff or employees": {"Impact": 2},
                "Customers or clients": {"Impact": 2},
                "Third-party stakeholders": {"Impact": 2},
                "Regulatory bodies": {"Impact": 3},
                "General public": {"Impact": 3},
                "Vulnerable populations": {"Impact": 4},
                "Other": {"Impact": 1}
            },
            "notes": "Each selected group contributes its Impact value to the total."
        }
    }
    
    # A3.4 - Notification Methods → Control Effectiveness (Negative - improves control)
    schema["questions"]["A3_4"] = {
        "id": "A3_4",
        "text": "How are affected parties notified that AI is involved in decisions?",
        "type": "multiselect",
        "domains": ["Transparency", "Accountability"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "Explicit disclosure in interface": {"Control_Effectiveness": -3},
                "Terms of service or policy": {"Control_Effectiveness": -1},
                "On-demand explanation available": {"Control_Effectiveness": -2},
                "Training or documentation": {"Control_Effectiveness": -2},
                "No notification": {"Control_Effectiveness": 0}
            }
        }
    }
    
    # A3.5 - Staff Impacts with Severity → Impact (Two-part question)
    schema["questions"]["A3_5"] = {
        "id": "A3_5",
        "text": "What impacts could the system have on staff? (Select impacts and rate severity 1-5)",
        "type": "multiselect_with_severity",
        "domains": ["Fairness", "Accountability"],
        "scoring": {
            "target_metric": "Impact",
            "part_a": "A3_5a",
            "part_b": "A3_5b",
            "impacts": {
                "Job role changes": {"base_impact": 2},
                "Workload redistribution": {"base_impact": 1},
                "Performance monitoring": {"base_impact": 2},
                "Career progression": {"base_impact": 3},
                "Job security": {"base_impact": 4},
                "Skills requirements": {"base_impact": 2},
                "No significant impact": {"base_impact": 0}
            },
            "severity_multiplier": "A3_5b (rating 1-5)",
            "formula": "Impact = sum(selected_base_impacts) × (severity_rating / 3)",
            "notes": "Severity rating scales the cumulative impact. Rating of 3 is neutral, 5 doubles impact, 1 reduces to one-third."
        }
    }
    
    # A3.6 - Group Impacts with Severity → Impact (Two-part question)
    schema["questions"]["A3_6"] = {
        "id": "A3_6",
        "text": "What impacts could the system have on external groups? (Select impacts and rate severity 1-3)",
        "type": "multiselect_with_severity",
        "domains": ["Fairness", "Accountability"],
        "scoring": {
            "target_metric": "Impact",
            "part_a": "A3_6a",
            "part_b": "A3_6b",
            "impacts": {
                "Service quality changes": {"base_impact": 2},
                "Access to services": {"base_impact": 3},
                "Financial impact": {"base_impact": 3},
                "Privacy concerns": {"base_impact": 3},
                "Trust and perception": {"base_impact": 2},
                "Legal or compliance risk": {"base_impact": 4},
                "No significant impact": {"base_impact": 0}
            },
            "severity_multiplier": "A3_6b (rating 1-3)",
            "formula": "Impact = sum(selected_base_impacts) × (severity_rating / 2)",
            "notes": "Severity rating scales the cumulative impact. Rating of 2 is neutral, 3 increases impact by 50%, 1 cuts it in half."
        }
    }
    
    # ============================================================================
    # SECTION A4: Outputs and Actions
    # ============================================================================
    
    # A4.1 - Primary Outputs → Impact
    schema["questions"]["A4_1"] = {
        "id": "A4_1",
        "text": "What are the primary outputs of the AI system?",
        "type": "multiselect",
        "domains": ["Accountability", "Transparency"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Recommendations": {"Impact": 2},
                "Classifications": {"Impact": 2},
                "Predictions": {"Impact": 2},
                "Risk scores": {"Impact": 3},
                "Automated decisions": {"Impact": 4},
                "Content generation": {"Impact": 2},
                "Data insights": {"Impact": 1},
                "Alerts or notifications": {"Impact": 2},
                "Reports": {"Impact": 1},
                "Other": {"Impact": 1}
            }
        }
    }
    
    # A4.2 - External Outputs Without Review → Likelihood
    schema["questions"]["A4_2"] = {
        "id": "A4_2",
        "text": "Are outputs sent to external systems without human review?",
        "type": "yes_no",
        "domains": ["Accountability", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Likelihood",
            "options": {
                "No": {"Likelihood": 0},
                "Yes": {"Likelihood": 2}
            }
        }
    }
    
    # A4.3 - Output BIL → Impact
    schema["questions"]["A4_3"] = {
        "id": "A4_3",
        "text": "What is the Business Impact Level (BIL) of the system outputs?",
        "type": "single_select",
        "domains": ["Privacy Protection and Security"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Official": {"Impact": 0},
                "Official: Sensitive": {"Impact": 1},
                "Protected": {"Impact": 2},
                "Highly Protected": {"Impact": 3},
                "Secret": {"Impact": 4},
                "Top Secret": {"Impact": 5}
            }
        }
    }
    
    # A4.4 - Output Tracking → Control Effectiveness
    schema["questions"]["A4_4"] = {
        "id": "A4_4",
        "text": "How are system outputs tracked?",
        "type": "multiselect",
        "domains": ["Accountability", "Contestability"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "Stored in database": {"Control_Effectiveness": -2},
                "Logged in audit system": {"Control_Effectiveness": -3},
                "Logged in CRM/case system": {"Control_Effectiveness": -2},
                "Logged in activity logs": {"Control_Effectiveness": -2},
                "Retention based on policy": {"Control_Effectiveness": -1},
                "Not currently tracked": {"Control_Effectiveness": 0}
            },
            "notes": "Output tracking improves control effectiveness and enables contestability. 'Not currently tracked' should be flagged as a risk."
        }
    }
    
    # A4.5 - Output Risks → Impact & Likelihood (Dual-metric, Two-part)
    schema["questions"]["A4_5"] = {
        "id": "A4_5",
        "text": "Are there risks associated with unauthorized access to system outputs?",
        "type": "yes_no_with_options",
        "domains": ["Privacy Protection and Security", "Reliability and Safety"],
        "scoring": {
            "target_metric": "Impact and Likelihood",
            "modifier_type": "dual",
            "options": {
                "No": {
                    "Impact": 0,
                    "Likelihood": 0
                },
                "Yes": {
                    "Impact": 0,
                    "Likelihood": 0,
                    "sub_question": "A4_5_scenarios",
                    "risk_scenarios": {
                        "Misrouted outputs": {
                            "Impact": 2,
                            "Likelihood": 2
                        },
                        "Excessive data exposure": {
                            "Impact": 3,
                            "Likelihood": 3
                        },
                        "Output reveals sensitive attributes": {
                            "Impact": 4,
                            "Likelihood": 4
                        },
                        "Outputs sent to incorrect system": {
                            "Impact": 3,
                            "Likelihood": 3
                        },
                        "Injection or poisoning risk": {
                            "Impact": 4,
                            "Likelihood": 4
                        }
                    }
                }
            },
            "notes": "Two-part question. If 'No', no additional risk. If 'Yes', each selected risk scenario applies both Impact and Likelihood modifiers."
        }
    }
    
    # A4.6 - Regulated Output Data Types → Impact
    schema["questions"]["A4_6"] = {
        "id": "A4_6",
        "text": "What types of regulated or sensitive data are included in system outputs?",
        "type": "multiselect",
        "domains": ["Privacy Protection and Security", "Fairness"],
        "scoring": {
            "target_metric": "Impact",
            "options": {
                "Personal": {"Impact": 2},
                "Sensitive": {"Impact": 3},
                "Financial": {"Impact": 3},
                "Health": {"Impact": 4},
                "Child-related": {"Impact": 5},
                "Law enforcement": {"Impact": 5},
                "Indigenous data": {"Impact": 5},
                "Confidential government data": {"Impact": 4},
                "Operationally sensitive data": {"Impact": 3}
            },
            "notes": "Each selected data type contributes its Impact value. Multiple selections are cumulative."
        }
    }
    
    # A4.7 - PII in Outputs (Text field - LLM classification pending)
    schema["questions"]["A4_7"] = {
        "id": "A4_7",
        "text": "Who has access to personally identifiable information (PII) in system outputs?",
        "type": "text",
        "domains": ["Privacy Protection and Security"],
        "scoring": {
            "target_metric": "TBD",
            "logic": "LLM-assisted classification required",
            "notes": "Text response will be analyzed using LLM to determine appropriate Impact/Likelihood modifiers."
        }
    }
    
    # A4.8 - Legal/Regulatory Actions (Text field - LLM classification pending)
    schema["questions"]["A4_8"] = {
        "id": "A4_8",
        "text": "Could system outputs trigger legal, regulatory, or compliance actions?",
        "type": "text",
        "domains": ["Accountability", "Compliance"],
        "scoring": {
            "target_metric": "TBD",
            "logic": "LLM-assisted classification required",
            "notes": "Text response will be analyzed using LLM to determine appropriate Impact/Likelihood modifiers."
        }
    }
    
    # ============================================================================
    # SECTION A5: Governance and Oversight
    # ============================================================================
    
    # A5.1 - Accountability Role → Control Effectiveness
    schema["questions"]["A5_1"] = {
        "id": "A5_1",
        "text": "Who is accountable for the AI system's performance and decisions?",
        "type": "single_select",
        "domains": ["Accountability"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "Product owner": {"Control_Effectiveness": -2},
                "System owner": {"Control_Effectiveness": -3},
                "Executive sponsor": {"Control_Effectiveness": -2},
                "Service manager": {"Control_Effectiveness": -3},
                "Data custodian": {"Control_Effectiveness": -3},
                "Governance committee": {"Control_Effectiveness": -4},
                "AI oversight board": {"Control_Effectiveness": -4}
            },
            "notes": "Clear accountability structures improve control effectiveness. Higher-level oversight (committees, boards) provide stronger governance."
        }
    }
    
    # A5.2 - Tracking Method (Text field - LLM classification pending)
    schema["questions"]["A5_2"] = {
        "id": "A5_2",
        "text": "How is system performance tracked and reported?",
        "type": "text",
        "domains": ["Accountability", "Transparency"],
        "scoring": {
            "target_metric": "TBD",
            "logic": "LLM-assisted classification required",
            "notes": "Text response will be analyzed using LLM to determine appropriate Control Effectiveness modifiers."
        }
    }
    
    # A5.3 - Monitoring & Evaluation Processes → Control Effectiveness
    schema["questions"]["A5_3"] = {
        "id": "A5_3",
        "text": "What monitoring and evaluation processes are in place? (Select all that apply)",
        "type": "multiselect",
        "domains": ["Reliability and Safety", "Accountability"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "Regular system audits": {"Control_Effectiveness": -3},
                "Continuous performance monitoring": {"Control_Effectiveness": -4},
                "User feedback collection": {"Control_Effectiveness": -2},
                "Periodic stakeholder reviews": {"Control_Effectiveness": -2},
                "Independent evaluation": {"Control_Effectiveness": -4}
            },
            "notes": "Monitoring and evaluation processes improve control effectiveness. Multiple selections are cumulative."
        }
    }
    
    # A5.4 - Monitoring Frequency → Control Effectiveness
    schema["questions"]["A5_4"] = {
        "id": "A5_4",
        "text": "How frequently will monitoring and evaluation occur?",
        "type": "single_select",
        "domains": ["Reliability and Safety"],
        "scoring": {
            "target_metric": "Control_Effectiveness",
            "modifier_type": "negative",
            "options": {
                "Weekly": {"Control_Effectiveness": -4},
                "Monthly": {"Control_Effectiveness": -3},
                "Quarterly": {"Control_Effectiveness": -2},
                "Annually": {"Control_Effectiveness": -1},
                "Event-driven": {"Control_Effectiveness": -3}
            },
            "notes": "More frequent monitoring improves control effectiveness. Weekly monitoring provides the strongest control."
        }
    }
    
    return schema


def save_schema_to_file(schema, output_path):
    """Save the schema to a JSON file"""
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2)
    print(f"✅ Schema saved to: {output_path}")


if __name__ == "__main__":
    # Generate the complete schema
    schema = generate_complete_scoring_schema()
    
    # Save to persistent location
    output_path = Path("/app/backend/faira_scoring_schema.json")
    save_schema_to_file(schema, output_path)
    
    # Print summary
    print(f"\n📊 Schema Summary:")
    print(f"   Total Questions: {len(schema['questions'])}")
    print(f"   Sections Covered: A1, A2, A3, A4 (partial)")
    print(f"   Special Factors: AutonomyFactor, DataQualityFactor, ExpertiseFactor")
    print(f"\n✅ Ready for next questions: A4.3 onwards, A5, B1-B8")
