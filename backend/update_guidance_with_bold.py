import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def update_guidance_with_bold():
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'am_ai_safe_db')
    
    print(f"Connecting to: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update SA-4 with proper bold formatting
    result_sa4 = await db.questions.update_one(
        {"code": "SA-4"},
        {"$set": {
            "additional_guidance": "**Additional Guidance: Handling Conflicts Between AI Actions and Human Safety Requirements**\n\nAI systems operating in dynamic or safety-critical environments must be designed to ensure that human safety always takes precedence over automated decision-making. This includes having safeguards that prevent the AI from taking actions that could cause harm, escalate risk, or violate established safety protocols.\n\nTo manage this effectively:\n\n- Establish **clear, documented safety protocols** that define how the system must behave when safety thresholds are reached.\n- Implement **fail-safe mechanisms**, such as controlled shutdowns, fallback actions, or degraded-mode operation when abnormal behaviour is detected.\n- Provide **human override capabilities** (e.g., kill switches, manual review modes, escalation alerts) to ensure that humans maintain ultimate control over the system.\n- Maintain **escalation procedures** describing who is notified and what actions are taken when a safety conflict arises.\n\nIn addition, modern safety expectations require **proactive validation**, not just reactive mitigation.\n\n**Include scenario-based testing and simulation of edge cases, failure modes, misuse scenarios, and unintended behaviours as part of your overall safety validation process.**\n\nThis ensures your system remains safe under a wide range of real-world and adversarial conditions."
        }}
    )
    print(f"✅ Updated SA-4 with bold formatting: {result_sa4.modified_count} document(s)")
    
    # Update IN-3 with proper bold formatting
    result_in3 = await db.questions.update_one(
        {"code": "IN-3"},
        {"$set": {
            "additional_guidance": "**Additional Guidance: Auditing for Exclusionary Outcomes and Unintended Group Impacts**\n\nInclusivity requires ensuring that your AI system provides equitable outcomes for all users, including diverse demographic groups, cultural backgrounds, linguistic communities, and users with disabilities. Auditing your system for exclusionary outcomes helps identify whether any group is disadvantaged or unintentionally excluded.\n\nTo assess inclusivity effectively:\n\n- Review outcomes across **multiple demographic and cultural groups** to identify unequal impacts.\n- Analyse patterns in errors, false positives/negatives, or service quality that may disproportionately affect vulnerable or underrepresented populations.\n- Perform **regular, structured audits** rather than relying solely on user complaints or ad-hoc testing.\n- Use **qualitative and quantitative methods**, including user research, fairness metrics, and stakeholder feedback.\n\nIn addition, modern inclusivity standards emphasise the need to evaluate **broader accessibility and cultural context**:\n\n**Ensure audits consider cultural, linguistic, and accessibility requirements to capture exclusionary impacts across a diverse range of user groups.**\n\nProactive auditing ensures your AI system better supports equitable, inclusive outcomes in real-world usage."
        }}
    )
    print(f"✅ Updated IN-3 with bold formatting: {result_in3.modified_count} document(s)")
    
    # Update SU-1 with proper bold formatting
    result_su1 = await db.questions.update_one(
        {"code": "SU-1"},
        {"$set": {
            "additional_guidance": "**Additional Guidance: Assessing the Environmental Impact of Training and Running AI Systems**\n\nAI systems can consume significant computational resources during both training and deployment. Understanding the environmental impact helps organisations manage energy use, reduce carbon emissions, and operate more sustainably.\n\nKey considerations include:\n\n- Measuring energy consumption, compute hours, and hardware utilisation during development and deployment.\n- Tracking the **carbon footprint** associated with training large models or running inference at scale.\n- Using cloud or data-centre providers that support **renewable energy sources** or that publish environmental transparency reports.\n- Optimising model architectures, batch sizes, resource allocation, and hardware choices for **energy efficiency**.\n\nTo ensure full lifecycle visibility, incorporate impact measurement into both early and operational phases:\n\n**Assess environmental impact across both training and inference workloads to capture the full lifecycle footprint of your AI system.**\n\nDocumenting and reviewing environmental metrics over time supports more sustainable AI practices and aligns with growing regulatory and industry expectations."
        }}
    )
    print(f"✅ Updated SU-1 with bold formatting: {result_su1.modified_count} document(s)")
    
    # Update AC-3 with proper bold formatting
    result_ac3 = await db.questions.update_one(
        {"code": "AC-3"},
        {"$set": {
            "additional_guidance": "**Additional Guidance: Defining and Assigning Roles for AI Risk, Ethics, and Compliance**\n\nClear accountability is a foundational principle of Responsible AI. Assigning roles ensures that individuals are responsible for overseeing ethical use, risk management, and compliance throughout the AI system's lifecycle.\n\nTo establish effective accountability structures:\n\n- Define and document responsibilities for AI oversight, including governance, ethics, system performance, and risk management.\n- Ensure assigned individuals understand their roles and have the required authority to enforce policies or halt unsafe activities.\n- Provide visibility into decision-making processes, including who approves model changes, who validates data quality, and who assesses system risks.\n- Regularly review and update role assignments to keep pace with organisational, regulatory, or system changes.\n\nModern AI frameworks emphasise clarity and traceability:\n\n**Clearly document and assign responsibilities such as system owner, risk owner, and model steward, and review these roles periodically to maintain effective oversight.**\n\nA well-defined accountability model reduces ambiguity and strengthens governance across the AI lifecycle."
        }}
    )
    print(f"✅ Updated AC-3 with bold formatting: {result_ac3.modified_count} document(s)")
    
    print("\n✅ All additional guidance updated with proper bold formatting!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_guidance_with_bold())
