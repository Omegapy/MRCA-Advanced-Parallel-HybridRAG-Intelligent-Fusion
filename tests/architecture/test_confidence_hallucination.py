# -------------------------------------------------------------------------
# File: test_confidence_hallucination.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/architecture/test_confidence_hallucination.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Implementation of Test Case 5 from Module 6 testing plan:
# "Confidence Score & Hallucination – Overall Architecture Evaluation (APH)"
# 
# Tests that the system detects unsupported/off-domain prompts and assigns
# correct confidence levels, preventing AI hallucinations in regulatory context.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Test Case 5: Confidence Score & Hallucination (Architecture Evaluation)

From Module 6 Testing Plan:
Input: Off-domain prompt "What sound does a dog make?"
Expected: Pre-made message explaining off-domain query handling; in-domain queries answered with high final confidence
Failure: Low confidence score or hallucinated off-domain answer
"""

import pytest
import asyncio
from typing import Dict, Any, List
import httpx
from unittest.mock import patch

from tests import ASR_THRESHOLDS, TEST_TIMEOUT_MEDIUM, SAMPLE_OFF_DOMAIN_QUERIES, SAMPLE_CFR_QUERIES


# =========================================================================
# Test Cases for Module 6 Test Case 5
# =========================================================================

@pytest.mark.architecture
@pytest.mark.requires_llm
class TestConfidenceAndHallucinationPrevention:
    """Test Case 5: Confidence Score & Hallucination Architecture Evaluation."""

    # Extended off-domain test queries
    OFF_DOMAIN_QUERIES = [
        {
            "query": "What sound does a dog make?",
            "category": "animal_sounds",
            "description": "Primary test case from Module 6"
        },
        {
            "query": "How do I cook pasta?",
            "category": "cooking",
            "description": "Cooking instructions - completely off-domain"
        },
        {
            "query": "What's the weather forecast for tomorrow?",
            "category": "weather",
            "description": "Weather information - off-domain"
        },
        {
            "query": "Tell me about the history of ancient Rome",
            "category": "history",
            "description": "Historical information - off-domain"
        },
        {
            "query": "How do I fix my car engine?",
            "category": "automotive",
            "description": "Automotive repair - off-domain"
        }
    ]

    # Mining-adjacent queries that might confuse the system
    DOMAIN_BOUNDARY_QUERIES = [
        {
            "query": "What safety equipment is used in construction?",
            "category": "construction_safety",
            "expected_behavior": "redirect_to_mining",
            "description": "Construction safety (adjacent to mining safety)"
        },
        {
            "query": "Tell me about oil drilling safety regulations",
            "category": "oil_drilling", 
            "expected_behavior": "redirect_to_mining",
            "description": "Oil drilling (adjacent to mining)"
        },
        {
            "query": "What are OSHA workplace safety standards?",
            "category": "osha_general",
            "expected_behavior": "redirect_to_msha",
            "description": "OSHA (related but different from MSHA)"
        }
    ]

    @pytest.mark.asyncio
    async def test_primary_off_domain_detection(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float]
    ):
        """
        Test Case 5: Primary off-domain query detection.
        
        Tests the exact query from Module 6 testing plan to ensure
        proper off-domain detection and appropriate response.
        """
        # Primary test query from Module 6
        test_query = "What sound does a dog make?"
        
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        assert response.status_code == 200, f"API request failed: {response.status_code}"
        response_data = response.json()
        
        # Validate response structure
        assert "response" in response_data, "Response missing 'response' field"
        assert "final_confidence" in response_data, "Response missing final confidence"
        
        response_text = response_data["response"]
        final_confidence = response_data["final_confidence"]
        
        # Test Case 5 specific validations
        
        # 1. Should NOT hallucinate about dog sounds
        dog_sound_indicators = ["woof", "bark", "ruff", "bow wow", "arf"]
        contains_dog_sounds = any(sound in response_text.lower() for sound in dog_sound_indicators)
        
        assert not contains_dog_sounds, (
            f"System hallucinated about dog sounds in response: {response_text[:200]}..."
        )
        
        # 2. Should indicate off-domain nature of query
        off_domain_indicators = [
            "msha", "mining", "regulatory", "compliance", "cfr",
            "not related to mining", "outside my expertise",
            "mining safety", "mine safety", "regulatory assistance"
        ]
        
        contains_domain_guidance = any(
            indicator in response_text.lower() 
            for indicator in off_domain_indicators
        )
        
        assert contains_domain_guidance, (
            f"Response should indicate mining/regulatory domain focus. "
            f"Response: {response_text[:200]}..."
        )
        
        # 3. Confidence should be low OR response should be domain-appropriate
        if final_confidence >= asr_thresholds["min_final_confidence"]:
            # If confidence is high, response should be domain-appropriate
            assert "mining" in response_text.lower() or "msha" in response_text.lower(), (
                f"High confidence ({final_confidence}) response should be domain-focused"
            )
        else:
            # Low confidence is acceptable for off-domain queries
            assert final_confidence < 0.7, (
                f"Off-domain query should have low confidence, got {final_confidence}"
            )
        
        print(f"✅ Test Case 5 Primary Test PASSED:")
        print(f"   No dog sound hallucination: {not contains_dog_sounds}")
        print(f"   Domain guidance provided: {contains_domain_guidance}")
        print(f"   Final confidence: {final_confidence:.3f}")
        print(f"   Response preview: {response_text[:150]}...")

    @pytest.mark.asyncio
    async def test_multiple_off_domain_queries(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float]
    ):
        """Test multiple off-domain queries for consistent behavior."""
        
        results = []
        
        for test_case in self.OFF_DOMAIN_QUERIES:
            print(f"\nTesting: {test_case['description']}")
            
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_case["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
            
            assert response.status_code == 200
            response_data = response.json()
            
            response_text = response_data["response"]
            final_confidence = response_data["final_confidence"]
            
            # Check for appropriate domain handling
            mining_indicators = ["mining", "msha", "cfr", "regulatory", "safety"]
            mentions_mining = any(indicator in response_text.lower() for indicator in mining_indicators)
            
            # Should either have low confidence OR redirect to mining domain
            appropriate_handling = (
                final_confidence < 0.7 or  # Low confidence
                mentions_mining            # Redirects to domain
            )
            
            results.append({
                "query": test_case["query"],
                "category": test_case["category"],
                "confidence": final_confidence,
                "mentions_mining": mentions_mining,
                "appropriate_handling": appropriate_handling,
                "response_length": len(response_text)
            })
            
            assert appropriate_handling, (
                f"Off-domain query '{test_case['query']}' not handled appropriately. "
                f"Confidence: {final_confidence}, Mentions mining: {mentions_mining}"
            )
        
        # Validate overall consistency
        low_confidence_rate = sum(1 for r in results if r["confidence"] < 0.7) / len(results)
        domain_redirect_rate = sum(1 for r in results if r["mentions_mining"]) / len(results)
        
        print(f"✅ Multi off-domain test PASSED:")
        print(f"   Low confidence rate: {low_confidence_rate:.1%}")
        print(f"   Domain redirect rate: {domain_redirect_rate:.1%}")
        print(f"   Average confidence: {sum(r['confidence'] for r in results) / len(results):.3f}")

    @pytest.mark.asyncio
    async def test_domain_boundary_queries(
        self, 
        backend_url: str
    ):
        """Test queries that are adjacent to mining domain."""
        
        for test_case in self.DOMAIN_BOUNDARY_QUERIES:
            print(f"\nTesting boundary case: {test_case['description']}")
            
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_case["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
            
            assert response.status_code == 200
            response_data = response.json()
            
            response_text = response_data["response"]
            final_confidence = response_data["final_confidence"]
            
            # These should redirect to mining/MSHA domain appropriately
            mining_redirect_indicators = [
                "msha", "mining safety", "mine safety", "cfr", "mining regulations"
            ]
            
            has_mining_redirect = any(
                indicator in response_text.lower() 
                for indicator in mining_redirect_indicators
            )
            
            # Should either redirect to mining domain or have reasonable confidence
            if test_case["expected_behavior"] == "redirect_to_mining":
                assert has_mining_redirect or final_confidence > 0.5, (
                    f"Domain boundary query should redirect to mining or have decent confidence. "
                    f"Query: {test_case['query']}, Confidence: {final_confidence}, "
                    f"Has mining redirect: {has_mining_redirect}"
                )

    @pytest.mark.asyncio
    async def test_in_domain_high_confidence(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float],
        sample_cfr_queries: List[str]
    ):
        """Test that in-domain queries maintain high confidence."""
        
        high_confidence_results = []
        
        for query in sample_cfr_queries:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": query,
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
            
            assert response.status_code == 200
            response_data = response.json()
            
            final_confidence = response_data["final_confidence"]
            high_confidence_results.append(final_confidence)
        
        # In-domain queries should generally have high confidence
        avg_confidence = sum(high_confidence_results) / len(high_confidence_results)
        high_confidence_rate = sum(1 for c in high_confidence_results if c >= asr_thresholds["min_final_confidence"]) / len(high_confidence_results)
        
        assert avg_confidence >= 0.7, (
            f"Average confidence for in-domain queries {avg_confidence:.3f} below threshold"
        )
        
        assert high_confidence_rate >= 0.6, (
            f"High confidence rate {high_confidence_rate:.1%} below 60% for in-domain queries"
        )
        
        print(f"✅ In-domain confidence test PASSED:")
        print(f"   Average confidence: {avg_confidence:.3f}")
        print(f"   High confidence rate: {high_confidence_rate:.1%}")

    @pytest.mark.asyncio
    async def test_hallucination_prevention_specific_domains(
        self, 
        backend_url: str
    ):
        """Test specific hallucination prevention for different domains."""
        
        hallucination_tests = [
            {
                "query": "What is the capital of France?",
                "avoid_terms": ["paris", "france", "capital", "city"],
                "description": "Geography knowledge"
            },
            {
                "query": "How do you make chocolate cake?",
                "avoid_terms": ["flour", "sugar", "bake", "oven", "recipe"],
                "description": "Cooking instructions"
            },
            {
                "query": "What are the symptoms of a cold?",
                "avoid_terms": ["fever", "cough", "runny nose", "symptoms"],
                "description": "Medical information"
            }
        ]
        
        for test in hallucination_tests:
            print(f"\nTesting hallucination prevention: {test['description']}")
            
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
            
            assert response.status_code == 200
            response_data = response.json()
            
            response_text = response_data["response"].lower()
            
            # Check that system doesn't hallucinate domain-specific information
            hallucination_detected = any(
                term in response_text for term in test["avoid_terms"]
            )
            
            # Should either avoid hallucination OR clearly indicate domain mismatch
            domain_indicators = ["mining", "msha", "regulatory", "cfr"]
            has_domain_focus = any(indicator in response_text for indicator in domain_indicators)
            
            appropriate_response = not hallucination_detected or has_domain_focus
            
            assert appropriate_response, (
                f"System may have hallucinated about {test['description']}. "
                f"Response: {response_data['response'][:200]}..."
            )


# =========================================================================
# ASR Validation Tests
# =========================================================================

@pytest.mark.architecture
class TestASRConfidenceValidation:
    """Architecture evaluation tests for ASR validation."""

    @pytest.mark.asyncio
    async def test_confidence_score_distribution(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float]
    ):
        """Test confidence score distribution across different query types."""
        
        test_categories = {
            "specific_cfr": [
                "What does 30 CFR 56.12016 say?",
                "Tell me about 30 CFR 75.380",
                "Requirements in 30 CFR 56.5005"
            ],
            "general_mining": [
                "What are methane monitoring requirements?",
                "Tell me about mining safety equipment",
                "Underground ventilation requirements"
            ],
            "off_domain": [
                "What sound does a dog make?",
                "How to cook pasta?",
                "Weather forecast"
            ]
        }
        
        confidence_distributions = {}
        
        for category, queries in test_categories.items():
            confidences = []
            
            for query in queries:
                async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                    response = await client.post(
                        f"{backend_url}/generate_parallel_hybrid",
                        json={
                            "user_input": query,
                            "fusion_strategy": "advanced_hybrid",
                            "template_type": "regulatory_compliance"
                        }
                    )
                
                assert response.status_code == 200
                response_data = response.json()
                confidences.append(response_data["final_confidence"])
            
            confidence_distributions[category] = {
                "avg": sum(confidences) / len(confidences),
                "min": min(confidences),
                "max": max(confidences),
                "values": confidences
            }
        
        # Validate expected confidence patterns
        # Specific CFR should have highest confidence
        assert confidence_distributions["specific_cfr"]["avg"] >= confidence_distributions["general_mining"]["avg"], (
            "Specific CFR queries should have higher confidence than general mining queries"
        )
        
        # Off-domain should have lowest confidence
        assert confidence_distributions["off_domain"]["avg"] <= confidence_distributions["general_mining"]["avg"], (
            "Off-domain queries should have lower confidence than mining queries"
        )
        
        print(f"✅ Confidence distribution test PASSED:")
        for category, stats in confidence_distributions.items():
            print(f"   {category}: avg={stats['avg']:.3f}, min={stats['min']:.3f}, max={stats['max']:.3f}")

    @pytest.mark.asyncio
    async def test_fusion_quality_correlation(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float]
    ):
        """Test correlation between fusion quality and final confidence."""
        
        test_queries = [
            "What are methane monitoring requirements in underground mines?",  # Should have good fusion
            "Tell me about 30 CFR 56.12016 grounding requirements",          # Specific citation
            "What sound does a dog make?"                                     # Off-domain
        ]
        
        fusion_results = []
        
        for query in test_queries:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": query,
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
            
            assert response.status_code == 200
            response_data = response.json()
            
            fusion_results.append({
                "query": query,
                "vector_confidence": response_data.get("vector_confidence", 0),
                "graph_confidence": response_data.get("graph_confidence", 0),
                "final_confidence": response_data["final_confidence"],
                "fusion_ready": response_data.get("fusion_ready", False)
            })
        
        # Validate fusion quality patterns
        for result in fusion_results:
            # When fusion is ready and both sources agree, final confidence should be high
            if (result["fusion_ready"] and 
                result["vector_confidence"] > 0.7 and 
                result["graph_confidence"] > 0.7):
                
                assert result["final_confidence"] >= asr_thresholds["min_confidence_fusion"], (
                    f"High fusion quality should result in high final confidence. "
                    f"Query: {result['query'][:50]}..., Final confidence: {result['final_confidence']}"
                )
        
        print(f"✅ Fusion quality correlation test PASSED:")
        for result in fusion_results:
            print(f"   {result['query'][:40]}...: final={result['final_confidence']:.3f}, "
                  f"vector={result['vector_confidence']:.3f}, graph={result['graph_confidence']:.3f}") 