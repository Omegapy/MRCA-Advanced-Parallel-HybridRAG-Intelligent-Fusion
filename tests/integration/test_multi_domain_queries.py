# -------------------------------------------------------------------------
# File: test_multi_domain_queries.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/integration/test_multi_domain_queries.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Implementation of Test Case 2 from Module 6 testing plan:
# "Multi-Domain Query - Component Integration Test"
# 
# Tests the fusion validity across multiple regulatory domains, validating
# that the system can retrieve and combine information from different CFR
# sections with appropriate fusion quality scores.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Test Case 2: Multi-Domain Query (Component Integration)

From Module 6 Testing Plan:
Input: "What are the regulations for underground drilling generating silica dust near diesel equipment?"
Expected: Cites multiple CFR sections with fusion_quality ≥ 0.70
Failure: Missing section/domain, conflicting passages, low fusion score
"""

import pytest
import asyncio
import time
from typing import Dict, Any, List, Set
import httpx
from unittest.mock import patch

from tests import ASR_THRESHOLDS, TEST_TIMEOUT_MEDIUM


# =========================================================================
# Test Cases for Module 6 Test Case 2
# =========================================================================

@pytest.mark.integration
@pytest.mark.requires_neo4j
@pytest.mark.requires_llm
class TestMultiDomainQueries:
    """Test Case 2: Multi-Domain Query Integration Tests."""

    # Complex multi-domain test queries that span multiple regulatory areas
    MULTI_DOMAIN_QUERIES = [
        {
            "query": "What are the regulations for underground drilling generating silica dust near diesel equipment?",
            "expected_domains": ["drilling", "silica", "dust", "diesel", "equipment", "underground"],
            "expected_cfr_areas": ["75", "56"],  # Underground (75) and surface/general (56)
            "description": "Primary test case from Module 6 - drilling + dust + diesel domains",
            "min_cfr_sections": 2
        },
        {
            "query": "What safety training and PPE requirements apply to miners working with explosives in underground ventilation areas?",
            "expected_domains": ["safety", "training", "ppe", "explosives", "ventilation", "underground"],
            "expected_cfr_areas": ["75", "77"],  # Underground coal + metal/nonmetal
            "description": "Training + PPE + explosives + ventilation domains",
            "min_cfr_sections": 3
        },
        {
            "query": "How do methane monitoring requirements interact with electrical equipment grounding in underground coal mines?",
            "expected_domains": ["methane", "monitoring", "electrical", "grounding", "underground", "coal"],
            "expected_cfr_areas": ["75"],  # Underground coal mines
            "description": "Methane monitoring + electrical safety domains",
            "min_cfr_sections": 2
        },
        {
            "query": "What are the combined requirements for noise control, respiratory protection, and equipment maintenance in surface mining operations?",
            "expected_domains": ["noise", "respiratory", "protection", "equipment", "maintenance", "surface"],
            "expected_cfr_areas": ["56"],  # Surface mines
            "description": "Noise + respiratory + maintenance domains",
            "min_cfr_sections": 3
        }
    ]

    # Boundary test cases - potentially challenging multi-domain scenarios
    BOUNDARY_MULTI_DOMAIN_QUERIES = [
        {
            "query": "What regulations apply when surface mining operations are near underground workings with shared ventilation systems?",
            "expected_domains": ["surface", "underground", "ventilation", "shared"],
            "description": "Surface + underground boundary case",
            "complex_fusion": True
        },
        {
            "query": "How do emergency evacuation procedures differ between coal and metal mines when considering equipment shutdown and communication systems?",
            "expected_domains": ["emergency", "evacuation", "coal", "metal", "equipment", "communication"],
            "description": "Coal vs metal mine comparison - complex domain interaction",
            "complex_fusion": True
        }
    ]

    @pytest.mark.asyncio
    async def test_primary_multi_domain_query(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float],
        performance_timer
    ):
        """
        Test Case 2: Primary multi-domain query from Module 6 testing plan.
        
        Tests the exact query specified in Module 6 to ensure proper
        multi-domain fusion with quality score validation.
        """
        # Primary test query from Module 6
        test_query = "What are the regulations for underground drilling generating silica dust near diesel equipment?"
        
        # Start performance timer
        performance_timer.start()
        
        # Make API request to Advanced Parallel Hybrid endpoint
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        # Stop performance timer
        elapsed_time = performance_timer.stop()
        
        # Basic response validation
        assert response.status_code == 200, f"API request failed: {response.status_code}"
        
        response_data = response.json()
        
        # Validate response structure
        assert "response" in response_data, "Response missing 'response' field"
        assert "vector_confidence" in response_data, "Response missing vector confidence"
        assert "graph_confidence" in response_data, "Response missing graph confidence"  
        assert "final_confidence" in response_data, "Response missing final confidence"
        assert "fusion_ready" in response_data, "Response missing fusion ready status"
        
        response_text = response_data["response"]
        
        # Test Case 2 specific validations
        
        # 1. Multiple CFR sections should be cited
        cfr_sections = self._extract_cfr_sections(response_text)
        assert len(cfr_sections) >= 2, (
            f"Expected multiple CFR sections, found {len(cfr_sections)}: {cfr_sections}"
        )
        
        # 2. Multiple regulatory domains should be addressed
        expected_domains = ["drilling", "silica", "dust", "diesel", "equipment", "underground"]
        domains_found = self._check_domain_coverage(response_text, expected_domains)
        domain_coverage = len(domains_found) / len(expected_domains)
        
        assert domain_coverage >= 0.6, (
            f"Insufficient domain coverage {domain_coverage:.1%}. "
            f"Found: {domains_found}, Expected: {expected_domains}"
        )
        
        # 3. Fusion quality validation (≥ 0.70)
        fusion_quality = self._calculate_fusion_quality(response_data)
        assert fusion_quality >= asr_thresholds["min_confidence_fusion"], (
            f"Fusion quality {fusion_quality:.3f} below threshold "
            f"{asr_thresholds['min_confidence_fusion']}"
        )
        
        # 4. Response should address interaction between domains
        interaction_indicators = [
            "underground drilling", "silica dust", "diesel equipment",
            "drilling operations", "dust control", "equipment safety"
        ]
        interaction_coverage = sum(
            1 for indicator in interaction_indicators 
            if indicator in response_text.lower()
        ) / len(interaction_indicators)
        
        assert interaction_coverage >= 0.4, (
            f"Insufficient domain interaction coverage {interaction_coverage:.1%}"
        )
        
        # 5. Fusion readiness should be true for multi-domain queries
        assert response_data["fusion_ready"] is True, (
            "Multi-domain queries should have fusion_ready=True"
        )
        
        print(f"✅ Test Case 2 Primary Test PASSED:")
        print(f"   CFR Sections Found: {len(cfr_sections)} - {list(cfr_sections)}")
        print(f"   Domain Coverage: {domain_coverage:.1%} - {domains_found}")
        print(f"   Fusion Quality: {fusion_quality:.3f}")
        print(f"   Interaction Coverage: {interaction_coverage:.1%}")
        print(f"   Response Time: {elapsed_time:.2f}s")

    @pytest.mark.asyncio
    async def test_multiple_multi_domain_scenarios(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float]
    ):
        """Test multiple multi-domain scenarios for consistency."""
        
        results = []
        
        for test_case in self.MULTI_DOMAIN_QUERIES:
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
            
            # Extract and validate CFR sections
            cfr_sections = self._extract_cfr_sections(response_text)
            min_sections = test_case.get("min_cfr_sections", 2)
            
            # Check domain coverage
            domains_found = self._check_domain_coverage(response_text, test_case["expected_domains"])
            domain_coverage = len(domains_found) / len(test_case["expected_domains"])
            
            # Calculate fusion quality
            fusion_quality = self._calculate_fusion_quality(response_data)
            
            results.append({
                "query": test_case["query"],
                "cfr_sections_found": len(cfr_sections),
                "cfr_sections": list(cfr_sections),
                "domain_coverage": domain_coverage,
                "fusion_quality": fusion_quality,
                "final_confidence": response_data["final_confidence"],
                "meets_requirements": (
                    len(cfr_sections) >= min_sections and
                    domain_coverage >= 0.5 and
                    fusion_quality >= asr_thresholds["min_confidence_fusion"]
                )
            })
            
            # Individual test assertions
            assert len(cfr_sections) >= min_sections, (
                f"Expected ≥{min_sections} CFR sections, found {len(cfr_sections)}"
            )
            
            assert domain_coverage >= 0.5, (
                f"Domain coverage {domain_coverage:.1%} below 50%"
            )
            
            assert fusion_quality >= asr_thresholds["min_confidence_fusion"], (
                f"Fusion quality {fusion_quality:.3f} below threshold"
            )
        
        # Overall consistency validation
        success_rate = sum(1 for r in results if r["meets_requirements"]) / len(results)
        avg_fusion_quality = sum(r["fusion_quality"] for r in results) / len(results)
        avg_cfr_sections = sum(r["cfr_sections_found"] for r in results) / len(results)
        
        assert success_rate >= 0.8, f"Multi-domain success rate {success_rate:.1%} below 80%"
        assert avg_fusion_quality >= 0.65, f"Average fusion quality {avg_fusion_quality:.3f} below threshold"
        
        print(f"✅ Multi-domain scenarios test PASSED:")
        print(f"   Success rate: {success_rate:.1%}")
        print(f"   Average fusion quality: {avg_fusion_quality:.3f}")
        print(f"   Average CFR sections: {avg_cfr_sections:.1f}")

    @pytest.mark.asyncio
    async def test_fusion_strategy_comparison(
        self, 
        backend_url: str,
        asr_thresholds: Dict[str, float]
    ):
        """Test different fusion strategies on multi-domain queries."""
        
        test_query = "What are the regulations for underground drilling generating silica dust near diesel equipment?"
        fusion_strategies = ["advanced_hybrid", "weighted_linear", "max_confidence", "adaptive_fusion"]
        
        strategy_results = {}
        
        for strategy in fusion_strategies:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_query,
                        "fusion_strategy": strategy,
                        "template_type": "regulatory_compliance"
                    }
                )
            
            assert response.status_code == 200
            response_data = response.json()
            
            response_text = response_data["response"]
            cfr_sections = self._extract_cfr_sections(response_text)
            fusion_quality = self._calculate_fusion_quality(response_data)
            
            strategy_results[strategy] = {
                "cfr_sections": len(cfr_sections),
                "fusion_quality": fusion_quality,
                "final_confidence": response_data["final_confidence"],
                "response_length": len(response_text)
            }
        
        # Validate that advanced_hybrid performs well for multi-domain queries
        advanced_result = strategy_results["advanced_hybrid"]
        assert advanced_result["fusion_quality"] >= asr_thresholds["min_confidence_fusion"], (
            f"Advanced hybrid fusion quality {advanced_result['fusion_quality']:.3f} below threshold"
        )
        
        # Compare strategies
        print(f"✅ Fusion strategy comparison PASSED:")
        for strategy, result in strategy_results.items():
            print(f"   {strategy}: quality={result['fusion_quality']:.3f}, "
                  f"cfr_sections={result['cfr_sections']}, "
                  f"confidence={result['final_confidence']:.3f}")

    @pytest.mark.asyncio
    async def test_boundary_multi_domain_cases(
        self, 
        backend_url: str
    ):
        """Test challenging boundary cases for multi-domain queries."""
        
        for test_case in self.BOUNDARY_MULTI_DOMAIN_QUERIES:
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
            
            # These complex cases should either:
            # 1. Provide comprehensive answers with good fusion
            # 2. Acknowledge complexity and provide appropriate guidance
            
            domains_found = self._check_domain_coverage(response_text, test_case["expected_domains"])
            domain_coverage = len(domains_found) / len(test_case["expected_domains"])
            
            complexity_indicators = [
                "complex", "multiple", "various", "different", "depends on",
                "both", "combination", "interaction", "coordination"
            ]
            
            acknowledges_complexity = any(
                indicator in response_text.lower() 
                for indicator in complexity_indicators
            )
            
            # Should either have good domain coverage OR acknowledge complexity
            appropriate_response = domain_coverage >= 0.5 or acknowledges_complexity
            
            assert appropriate_response, (
                f"Boundary case should have good domain coverage ({domain_coverage:.1%}) "
                f"or acknowledge complexity ({acknowledges_complexity})"
            )

    # Helper methods for validation
    
    def _extract_cfr_sections(self, text: str) -> Set[str]:
        """Extract CFR section references from response text."""
        import re
        
        # Pattern to match CFR references like "30 CFR 75.380" or "30 CFR 56.12016"
        cfr_pattern = r'30\s+CFR\s+(\d+)\.(\d+)'
        matches = re.finditer(cfr_pattern, text, re.IGNORECASE)
        
        sections = set()
        for match in matches:
            part = match.group(1)
            section = match.group(2)
            sections.add(f"30 CFR {part}.{section}")
        
        return sections
    
    def _check_domain_coverage(self, text: str, expected_domains: List[str]) -> List[str]:
        """Check which expected domains are covered in the response."""
        text_lower = text.lower()
        domains_found = []
        
        for domain in expected_domains:
            if domain.lower() in text_lower:
                domains_found.append(domain)
        
        return domains_found
    
    def _calculate_fusion_quality(self, response_data: Dict[str, Any]) -> float:
        """Calculate fusion quality score based on response metadata."""
        # Use final confidence as primary indicator of fusion quality
        final_confidence = response_data.get("final_confidence", 0.0)
        
        # If available, also consider vector and graph confidence agreement
        vector_conf = response_data.get("vector_confidence", 0.0)
        graph_conf = response_data.get("graph_confidence", 0.0)
        
        # Quality is higher when both sources contribute well
        if vector_conf > 0.0 and graph_conf > 0.0:
            # Weighted combination: final confidence with bonus for source agreement
            agreement_bonus = min(vector_conf, graph_conf) * 0.1
            return min(1.0, final_confidence + agreement_bonus)
        else:
            return final_confidence


# =========================================================================
# Failure Condition Tests
# =========================================================================

@pytest.mark.integration
class TestMultiDomainFailureConditions:
    """Test failure conditions for Test Case 2."""

    @pytest.mark.asyncio
    async def test_conflicting_domain_requirements(self, backend_url: str):
        """Test handling of potentially conflicting domain requirements."""
        
        # Query that might have conflicting requirements between domains
        conflicting_queries = [
            "What are surface mine ventilation requirements for underground operations?",  # Surface vs underground conflict
            "How do coal mine electrical requirements apply to metal mining equipment?",   # Coal vs metal conflict
        ]
        
        for query in conflicting_queries:
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
            
            response_text = response_data["response"]
            
            # Should either:
            # 1. Recognize and address the conflict appropriately
            # 2. Have lower confidence indicating uncertainty
            # 3. Provide clarification about domain boundaries
            
            conflict_awareness_indicators = [
                "surface mine", "underground", "coal mine", "metal mine",
                "different", "separate", "distinct", "specific to", "applies to"
            ]
            
            acknowledges_domains = any(
                indicator in response_text.lower() 
                for indicator in conflict_awareness_indicators
            )
            
            low_confidence = response_data["final_confidence"] < 0.7
            
            appropriate_handling = acknowledges_domains or low_confidence
            
            assert appropriate_handling, (
                f"Conflicting domain query should be handled appropriately. "
                f"Acknowledges domains: {acknowledges_domains}, "
                f"Low confidence: {low_confidence} ({response_data['final_confidence']:.3f})"
            )

    @pytest.mark.asyncio
    async def test_missing_domain_coverage(self, backend_url: str):
        """Test when system cannot adequately cover all requested domains."""
        
        # Query with domains that might not be well covered
        challenging_query = "What are the regulations for underwater mining operations with nuclear-powered equipment and space-grade materials?"
        
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": challenging_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Should handle gracefully with:
        # 1. Lower confidence for domains not well covered
        # 2. Focus on domains that are covered (mining-related aspects)
        # 3. Appropriate guidance about domain limitations
        
        response_text = response_data["response"].lower()
        final_confidence = response_data["final_confidence"]
        
        # Should focus on mining aspects and acknowledge limitations
        mining_focus = any(term in response_text for term in ["mining", "msha", "cfr"])
        limitation_acknowledgment = any(
            phrase in response_text for phrase in [
                "not covered", "not applicable", "beyond scope", "not regulated",
                "specialized", "specific guidance", "not addressed"
            ]
        )
        
        appropriate_response = (
            (mining_focus and final_confidence > 0.3) or  # Focus on relevant parts
            limitation_acknowledgment or                   # Acknowledge limitations
            final_confidence < 0.5                       # Low confidence for uncertainty
        )
        
        assert appropriate_response, (
            f"Should handle missing domain coverage appropriately. "
            f"Mining focus: {mining_focus}, Limitation ack: {limitation_acknowledgment}, "
            f"Confidence: {final_confidence:.3f}"
        ) 