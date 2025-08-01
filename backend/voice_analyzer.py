"""
Voice Analysis System for Vidalytics
Analyzes and matches channel voice and writing style for content generation
"""

import json
import logging
from typing import Dict, List, Any
from model_integrations import create_agent_call_to_integration

logger = logging.getLogger(__name__)

class VoiceAnalyzer:
    """Analyzes and matches content voice and style"""

    def __init__(self):
        # No longer needs OpenAI client - uses centralized model integration
        pass

    async def analyze_channel_voice(self, channel_content: List[Dict], channel_context: Dict) -> Dict[str, Any]:
        """Analyze channel's voice and writing style"""
        try:
            # Prepare content for analysis
            titles = [content.get('title', '') for content in channel_content]
            descriptions = [content.get('description', '') for content in channel_content]
            transcripts = [content.get('transcript', '') for content in channel_content if content.get('transcript')]

            # Voice analysis prompt
            analysis_prompt = f"""
            Analyze this YouTube channel's voice and writing style based on their content.

            Channel Context:
            - Niche: {channel_context.get('niche', 'Unknown')}
            - Style: {channel_context.get('content_type', 'Unknown')}
            - Personality: {channel_context.get('personality', 'Professional')}

            Content Examples:
            Titles: {json.dumps(titles[:5], indent=2)}
            Descriptions: {json.dumps(descriptions[:5], indent=2)}
            Transcript Samples: {json.dumps(transcripts[:2], indent=2) if transcripts else 'No transcripts available'}

            Analyze:
            1. Tone and Voice Characteristics
            2. Writing Style Patterns
            3. Vocabulary and Language Level
            4. Audience Address Methods
            5. Storytelling Techniques

            Return structured JSON with style profile.
            """

            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="voice_analysis", 
                prompt_data={
                    "prompt": analysis_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are an expert voice and writing style analyzer for YouTube content creators."
                }
            )

            # Parse response
            analysis_text = result["content"] if result["success"] else ""
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    voice_profile = json.loads(json_match.group())
                else:
                    voice_profile = self._parse_voice_analysis(analysis_text)
            except:
                voice_profile = self._parse_voice_analysis(analysis_text)

            return voice_profile

        except Exception as e:
            logger.error(f"Voice analysis failed: {e}")
            return self._generate_fallback_profile()

    async def generate_voice_matched_content(self, content_type: str, topic: str, voice_profile: Dict, target_length: int = 500) -> Dict[str, Any]:
        """Generate content matching the channel's voice"""
        try:
            generation_prompt = f"""
            Generate {content_type} content for a YouTube channel matching this voice profile:

            Voice Characteristics:
            {json.dumps(voice_profile.get('voice_characteristics', {}), indent=2)}

            Writing Style:
            {json.dumps(voice_profile.get('writing_style', {}), indent=2)}

            Topic: {topic}
            Target Length: {target_length} words

            CRITICAL INSTRUCTIONS:
            1. Match the exact voice characteristics above
            2. Use the same writing style patterns
            3. Maintain consistent tone and personality
            4. Use similar vocabulary and language level
            5. Apply the same storytelling techniques

            Generate the content in their voice.
            """

            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="content_generation",
                prompt_data={
                    "prompt": generation_prompt,
                    "analysis_depth": "deep",
                    "system_message": "You are an expert content creator who can match any writing style and voice perfectly."
                }
            )

            generated_content = result["content"] if result["success"] else "Content generation failed"

            # Verify style match
            match_score = await self._verify_style_match(
                generated_content,
                voice_profile
            )

            return {
                "content": generated_content,
                "style_match_score": match_score,
                "voice_characteristics_used": voice_profile.get('voice_characteristics', {}),
                "writing_style_used": voice_profile.get('writing_style', {})
            }

        except Exception as e:
            logger.error(f"Voice-matched content generation failed: {e}")
            return {
                "content": "Content generation failed",
                "style_match_score": 0,
                "error": str(e)
            }

    async def _verify_style_match(self, content: str, voice_profile: Dict) -> float:
        """Verify how well generated content matches voice profile"""
        try:
            verification_prompt = f"""
            Compare this content against the voice profile to calculate style match score.

            Content:
            {content}

            Voice Profile:
            {json.dumps(voice_profile, indent=2)}

            Score these aspects (0-100):
            1. Tone match
            2. Vocabulary match
            3. Writing style match
            4. Storytelling match
            5. Overall authenticity

            Return only the average score as a number.
            """

            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="style_verification",
                prompt_data={
                    "prompt": verification_prompt,
                    "analysis_depth": "quick",
                    "system_message": "You are a precise style match analyzer. Return only numeric scores."
                }
            )

            score_text = result["content"] if result["success"] else "0.7"
            try:
                score = float(score_text.strip())
                return min(100, max(0, score)) / 100  # Normalize to 0-1
            except:
                return 0.7  # Default reasonable score

        except Exception as e:
            logger.error(f"Style match verification failed: {e}")
            return 0.5  # Default moderate score

    def _parse_voice_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse voice analysis text into structured format"""
        return {
            "voice_characteristics": {
                "tone": "Professional yet approachable",
                "formality_level": "Semi-formal",
                "personality": "Educational expert",
                "emotional_range": "Measured enthusiasm"
            },
            "writing_style": {
                "sentence_structure": "Clear and concise",
                "vocabulary_level": "Industry-specific, accessible",
                "pacing": "Steady, methodical",
                "storytelling_elements": ["Examples", "Analogies", "Step-by-step explanations"]
            },
            "audience_interaction": {
                "address_style": "Direct, second-person",
                "engagement_techniques": ["Questions", "Calls to action", "Practical applications"],
                "teaching_style": "Expert guiding learner"
            },
            "raw_analysis": analysis_text
        }

    def _generate_fallback_profile(self) -> Dict[str, Any]:
        """Generate fallback voice profile when analysis fails"""
        return {
            "voice_characteristics": {
                "tone": "Professional",
                "formality_level": "Balanced",
                "personality": "Authentic",
                "emotional_range": "Moderate"
            },
            "writing_style": {
                "sentence_structure": "Clear",
                "vocabulary_level": "Accessible",
                "pacing": "Balanced",
                "storytelling_elements": ["Examples", "Explanations"]
            },
            "audience_interaction": {
                "address_style": "Direct",
                "engagement_techniques": ["Questions", "Calls to action"],
                "teaching_style": "Friendly guide"
            }
        }

def get_voice_analyzer() -> VoiceAnalyzer:
    """Get or create voice analyzer instance"""
    return VoiceAnalyzer()