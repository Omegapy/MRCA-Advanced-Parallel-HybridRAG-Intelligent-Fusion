
---
---

# MRCA Development Documentation

Author:
Alexander Ricciardi   
Colorado State University Global   
CSC480: Capstone Computer Science  
Dr. Shaher Daoud  
Spring-D Semester June-August 2025  

This document provides a step-by-step process, organized into modules, for the development of MRCA.

© 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
License: Apache-2.0 | Technology: Advanced Parallel Hybrid RAG System

---
---

# Module 1 Capstone Milestone: Topic Approval

---

## Module 1 Capstone Milestone: Topic Approval

A student's computer science capstone project should illustrate what the student has learned in their bachelor's program, their career goals, and specialization if any, as well as showcase their ability to solve real-world problems using software and other computer science tools. The topic that I chose to reflect my learning, career goals, and specialization (future master's in AI) is a MSHA Regulatory Conversational Agent (MRCA) web application. The MRCA is an AI-powered conversational agent that retrieves information and answers questions about Mine Safety and Health Administration (MSHA) regulations, as outlined in Title 30 of the Code of Federal Regulations (CFR). It will allow users to quickly and easily access information and ask questions about MSHA regulations using a Large Language Model (LLM) combined with a GraphRAG hybrid search. 

## The Business Problem

The state of Wyoming, my place of residence, has a large mining industry in the form of surface coal mines. Although I am not a miner per se, I found myself on mine sites, as mines employed an array of contractors, from heavy equipment mechanics to copier technicians like me, to support mine operations, each in their own way. To be allowed on mine sites, I had to attend a 40-hour MSHA regulations training that legally certified me as a miner, and then every year, I needed to be recertified by attending an 8-hour refresher training. These trainings are essential as the MSHA Title 30 of the CFR is a massive and complex set of regulations that is constantly changing. Furthermore, intentionally or unintentionally not following MSHA regulations on mine sites can have serious consequences for businesses and individuals. These consequences range from a couple of hundred dollars fines to ten-thousand-dollar fines, to being banned from mine sites, to jail time. Therefore, being compliant is crucial, primarily for safety reasons, but also because MSHA agents patrol the mines and aggressively enforce the regulations.

The regulations being extensive, complex, and constantly changing create a challenge for contractors, miners, and safety managers, whose tasks need to be up-to-date and in compliance with the regulations. Even when I ensured beforehand that my task on a mine site would follow MSHA regulations, I found that once on-site, there was no easy way to check compliance if an unforeseen problem or question suddenly come to be. For example, just the printed manual “Code of Federal Regulations Title 30 Mineral Resources Parts 1 to 199 (MSHA), Revised as of July 1, 2022” from the United States Office of Federal Register (2023) has about 780 pages, and CFR Title 30 has 999 parts spread out in several printed manuals or/and sections. The sheer size and complexity of these manuals make them difficult to carry on sites and very challenging to search for information. Additionally, searching those manuals for information remains difficult even when they are saved digitally on a device. Using search engines such as Google is not a reliable method, as it is time-consuming. Similarly, using a generic LLM chatbot for fetching accurate information about MSHA regulations is not a reliable method, as they often provide just general information, but more specifically, they are prone to hallucinating, that is, they can provide plausible-sounding answers that are incorrect or entirely fabricated. Nonetheless, LLM can be incorporated into an agentic framework that utilizes a combination of vector embedding, GraphRAG (Graph Retrieval-Augmented Generation), and tool use. A Regulatory conversational agent web application can integrate these techniques, making it easily accessible (e.g., cell phone) that can not only quickly provide accurate information about MSHA regulations but also accurately explain them.

## The Solution

The MSHA Regulatory Conversational Agent (MRCA) web application will be a valuable tool for mine contractors, miners, and safety managers to access accurate information about MSHA regulations quickly. The MRCA application core implementation will be a GraphRAG (Retrieval-Augmented Generation) system utilizing a hybrid search approach that combines native vector search and traversal search. A GraphRAG is a RAG technique based on a knowledge graph. A knowledge graph is a structure that stores entities and their relationships, that is, contextual data. The graph’s contextual data can be queried and retrieved by an LLM, enabling it to generate accurate results based on entities and their relationships. The GraphRAG can use a hybrid search approach; it can use vector embedding for native vector search and knowledge graphs for entity and traversal search (context search). The GraphRAG hybrid search method has a Mean Reciprocal Rank (MRR) - mean accuracy - of 0.927, which is an improvement of 77.6% over the baseline RAG's score of 0.522 (Xu et al., 2024). A GraphRAG hybrid search method will be implemented in MRCA; however, a 92.70% mean accuracy score is not a 100% accuracy score; therefore, a notice should be posted that the agent is an informational tool designed to assist and guide users with MSHA regulatory questions and should not be used as a replacement for the official Title 30 CFR documentation. A Large Reasoning Model (LRM) will be utilized for generating the knowledge graphs, probably Gemini 2.5pro. The steps of building a knowledge graph using an LRM are as follows:

- Gather the data  
- Chunk the data  
- Vectorize the data  
- Pass the data to an LLM or LRM to extract nodes and relationships  
- Use the output to generate the graph  

(GraphAcademy, n.d.)

### Table 1  
**MRCA Web Application Requirements**

| Component / Task | Frameworks / Requirements |
|------------------|----------------------------|
| **Programming Language** | Python |
| **Data Collection** | **Title 30 of the Code of Federal Regulations (CFR) from GovInfo.gov**, PDF data, for one-year bulk download. eCFR website for daily updates. |
| **Source data storage** | Neo4j |
| **Parsing & chunking** | LangChain’s RecursiveCharacterTextSplitter |
| **Vectorization** | OpenAI's text-embedding-ada-002 |
| **Knowledge Graph & Backend** | LangChain’s LLMGraphTransformer with Gemini 2.5pro |
| **Database (graph & vectors)** | Neo4j AuraDB |
| **Final step in creating the graph** | Cypher MERGE queries in Neo4j |
| **Backend API** | FastAPI |
| **Core component & prompt processing** | LangChain + GraphCypherQAChain |
| **Search** | Neo4j's native vector search + graph traversal |
| **Answer Generation** | OpenAI GPT-4o |
| **User Interface (UI)** | Streamlit |
| **Security** | Environment variables, read-only DB, logging module, subscription plan |
| **Deployment** | Streamlit Community Cloud; Docker future |

Note: The table illustrates the design phases/steps, components, and requirements/frameworks that will be used to build the MRCA web application.

## Project Timeline Scope

The timeline to design and implement the MRCA web application is only 8 weeks long, and when combined with attending school full time and having a job, I need to carefully define the scope of the project's initial version, so I can successfully deliver the project. For example, see Table 2, the MSHA regulation source can be accessed from two different and raw mine operational data can be accessed from the MSHA website itself. For this project, for the length of this course, I am only planning to use the data from the GovInfo.gov. However, if time allows it, and after getting authorized by the professor, I may integrate the raw operational mine data as examples of accidents, violations, and penalties to be searchable alongside the official MSHA regulations.

### Table 2  
**Data Sources for the MRCA Project**

| Source | Content | Update Frequency | Legal Status | Use For | How to Download |
|--------|---------|------------------|--------------|---------|-----------------|
| **GovInfo.gov** | Official Title 30 CFR manual | Annually | Official, legally binding | Legal research, verification, and historical reference | Annual in PDF or XML formats |
| **eCFR.gov** | Unofficial current update compilation | Daily | Unofficial | For most current version | Print to PDF or save as HTML |
| **MSHA.gov** | Raw mine operational data | Daily, weekly, quarterly | Not applicable | Accident/violation/penalty analysis | CSV or TXT format or custom reports |

Note: The table illustrates the different sources for the MRCA project by providing a description of their content, update frequency, legal status, usage, and download methods.

## Topic Summary

The goal of the MSHA Regulatory Conversational Agent (MRCA) web application is to allow users to quickly and easily access information about MSHA regulations by leveraging LLMs and GraphRAG hybrid search method for accuracy. Moreover, the main goal of the overall project is to illustrate what I learned throughout my Computer Science bachelor's program at Colorado State University Global (CSU Global), my career goals, and to be a bridge between my bachelor's and my future specialization in AI and Machine Learning (ML) through a Master’s in Science’s program at CSU Global. It will showcase my ability to solve real-world problems using software and computer science techniques. The MRAC web application is a well-rounded project that will be a valuable portfolio project.

## References

United States Office of Federal Register (2023, October 23). *Code of Federal Regulations Title 30 Mineral Resources Parts 1 to 199 (MSHA), Revised as of July 1, 2022*. ISBN-13: 979-8399878225

GraphAcademy (n.d.). *Building Knowledge Graphs with LLMs* [Online Course]. Neo4j. https://graphacademy.neo4j.com/courses/llm-knowledge-graph-construction/1-knowledge-graphs/1-knowledge-graph/

Xu, Z., Cruz, M. J., Guevara, M., Wang, T., Deshpande, M., Wang, X., & Li, Z. (2024, July 11). *Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering*. SIGIR '24. https://doi.org/10.1145/3626772.366137

---
---

# Module 2 Capstone Milestone: Project Proposal

---

## Module 2 Capstone Milestone: Project Proposal

Title 30 of the Code of Federal Regulations (CFR), also referred to as the Mine Safety and Health Administration (MSHA) regulations, is a set of federal regulations that govern the United States mining industry. These regulations ensure that mine operations are safe and protect individuals. This document is a proposal for the development of an MSHA Regulatory Conversational Agent (MRCA) that will quickly and accurately access information about MSHA regulations. 

## The Problem

The sheer size and complexity of the CFR Title 30 make it very difficult for mine workers to find quick and accurate answers to specific questions about MSHA regulations, especially when on a mine site. Methods such as searching through large printed or digital volumes are time-consuming and very inefficient, and generic search engines (e.g., Google) and large language models (LLMs) often provide unreliable or fabricated information (Ricciardi, 2025). A possible solution to this problem is an MRCA. 

## The Solution

MRCA is an AI-powered web application that will provide a quick, reliable, and easy way to query MSHA regulations using natural language by combining an LLM with a GraphRAG hybrid search. The GraphRAG is “a powerful technique that enhances downstream task execution by retrieving additional information, such as knowledge, skills, and tools from external sources” (Han et al., 2025, p.1). The GraphRAG hybrid search, also called HybridRAG, is defined as a novel approach to the Retrieval Augmentation Generation (RAG) technique that combines GraphRAG and VectorRAG techniques to enhance question-answer systems for information extraction (Sarmah et al., 2024). HybridRAG extracts contextual relational data from a knowledge graph using traversal search, and it extracts contextual semantic information for the vector store using semantic search. This hybrid approach to RAG significantly decreases LLM “hallucinations” with an accuracy of 92.7%, which is a significant improvement over baseline RAG (Vector RAG) with an accuracy of 52.2% (Xu et al., 2024). This combination of LLM and GraphRAG hybrid search is the core component of the MRCA, allowing it to provide users with a quick and easy way to access MSHA regulation information using natural language.

## MRCA System Overview

MRCA will be designed to be modular, meaning that the application will be organized as a "logical grouping of related code" (Richards & Ford, 2020, p.40) distributed within a file structure and classes. The Title 30 CFR data will be downloaded from GovInfo.gov in PDF format, distributed in three volumes. Gemini 2.5 pro will be used to generate the knowledge graph and to chunk and vectorize the download Title 30 CFR data, and the resulting graph and vector store will be stored in a Neo4j Aura Database. OpenAI 4o will act as the conversational agent, handling the interaction with the user, embedding user prompts to perform semantic search. Then, based on the semantic search results, it will generate Cypher code that will be used to perform the traversal search. The application’s front-end will be handled by a web chat system based on the framework Streamlit. The application’s back end will be handled by FastAPI web framework for RESTful API. The project will be coded in Python 3.12.1 and deployed on Streamlit Community Cloud. The development process will use the iterative methodology Kanban, git/GitHub for version control, and Docker for environment containerization. 

## MRCA Timeline and Major Components

The project must be implemented within eight weeks. The table below illustrates the timeline and describes the project development phases and related components.

### Table 1  
**Project Phases and Timeline**

| Timeline and Phases         | Phase Description and Major Component                                                                                                                                                      |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Phase 1** <br>Backend Setup <br>**Weeks 1–2**  | This phase consists of setting up the environment and Docker; gathering the data, developing the `cfr_downloader.py` script to download the MSHA data; and developing the `build_graph.py` script to chunk, vectorize, and graph the downloaded data. |
| **Phase 2** <br>Agent & Tools Setup <br>**Weeks 3–4** | This phase sets up the agent and its tools, such as `tools/vector.py` for vector search and `tools/cypher.py` for graph query. It will also implement `llm.py` for LLM connection and initialize the FastAPI implementation. |
| **Phase 3** <br>Agent & Tool Testing <br>**Weeks 5–6** | This phase tests the agent and its tools. It implements `agent.py`, a ReAct agent for orchestrating tools, and `tools/general.py` for MSHA regulations domain restriction. |
| **Phase 4** <br>Testing, Optimization, & Deployment <br>**Weeks 7–8** | This phase finalizes the Streamlit user interface (`bot.py`), performs end-to-end testing, optimizes, and deploys the app. It also cleans/retests the code, finishes testing the FastAPI integration, and finishes project documentation. |

Note: The table describes the project’s phases, related major components, and timeline.  
The development process shown in the Table seems to be strictly sequential; however, the process is iterative as each component is built and tested in iterative steps throughout the phases.

## Conclusion

The MRCA web application is a solution for accessing quickly and easily accurate information about MSHA regulations. It will combine the functionality of LLM with HybridRAG, which significantly reduces LLM hallucinations, making the combo a reliable method for information extraction. Although this RAG method has been shown to have an accuracy of 92.2%, MRCA should not be used as a replacement for the official Title 30 CFR documentation. Nonetheless, it is a valuable and practical tool for miners, contractors, and safety managers that provides quick and accurate access to MSHA regulations, helping them to stay informed, work safely, and comply with regulations.

## References

Han, H., Wang, Y., Shomer, H., Guo, K., Ding, J., Lei, Y., Halappanavar, M., Rossi, R. A., Mukherjee, S., Tang, X., He, Q., Hua, Z., Long, B., Zhao, T., Shah, N., Javari, A., Xia, Y., & Tang, J. (2025, January 25). *Retrieval-Augmented Generation With Graphs (GraphRAG)*. arXiv. https://arxiv.org/abs/2501.00309

Richards, M., & Ford, N. (2020). Chapter 4: Architecture Characteristics Defined. *Fundamentals of software architecture: An engineering approach* (pp. 39–56). O'Reilly Media.

Sarmah, B., Patel, S., Hall, B., Pasquali, S., Rao, R., & Mehta, D. (2024, August 9). *HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction*. arXiv. https://arxiv.org/abs/2408.04948

Ricciardi (2025, June 15). *Module 1 Capstone Milestone: Topic Approval* [Student Essay]. CSC480 Capstone Computer Science. CSU Global.

Xu, Z., Cruz, M. J., Guevara, M., Wang, T., Deshpande, M., Wang, X., & Li, Z. (2024, July 11). *Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering*. ACM Digital Library, SIGIR '24: Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, p. 2905–2909. https://doi.org/10.1145/3626772.366137

---
---

# Module 3 Capstone Milestone: Software Design

---

## Module 3 Capstone Milestone: Software Design

The MSHA Regulatory Conversational Agent, now renamed **Mining Regulatory Compliance Assistant (MRCA)**, is an AI-powered web application that will provide a quick, reliable, and easy way to query Mine Safety and Health Administration (MSHA) regulations using natural language. MRCA combines Large Language Models (LLMs) with an Advanced Parallel HybridRAG (HPA) technique to minimize LLM hallucinations. This paper describes the MRCA's architectural components, such as microservices through HTTP RESTful API using the FastAPI framework, and the Advanced Parallel HybridRAG system, which uses a Neo4j AuraDB knowledge graph (KG) with vector embedding attributes (vector index) database for semantic search, traversal search, and data retrieval.

## MRCA Architecture

After iterating through different architecture designs, the MRCA architecture evolved from a Modular Monolith Architecture using a sequential HybriRAG to a more advanced Microservice Backends-for-Frontends (BFF) architecture using an Advanced Parallel HybridRAG. Microservice BFF is an architecture that adds an abstraction layer (interface) between the frontend User Interface (UI) and the backend, retrieval data layer, that serves as micro-service for the UI (Abdelfattah & Cerny, 2023). 

The Advanced Parallel HybridRAG is a novel system that is similar to the HybridRAG concept. The HybridRAG is a RAG system that combines KG-based RAG techniques (GraphRAG) and VectorRAG techniques (Sarmah et al., 2024). The Advanced Parallel HybridRAG differs from the HybridRAG in that it does not choose between a vector-based search (VectorRAG) or a graph-based search (GraphRAG); instead, it executes both retrieval methods in parallel. Additionally, within the Neo4j AuraDB, KGs and vector embeddings are stored in the same database. MRCA stores vector embeddings as attributes on nodes within the KG. This approach enables the same Chunk nodes to be used as both VectorRAG - semantic node search (via the textEmbedding property) and GraphRAG - traversal search (via entity relationships).

See Figure 1 for an overview of the MRCA architecture.

[--Figure 1: MRCA Architecture Diagram--]  
*Note: The diagram illustrates the MRCA architecture with its core components and their data/control flow.*

## MRCA Advanced Parallel HybridRAG

The Advanced Parallel HybridRAG (APH) technique processes user prompts by using the VectorRAG and GraphRAG retrieval methods in parallel. In other words, within the APH parallel engine, the entirety of a user prompt is processed in parallel by both the VectorRAG and GraphRAG methods. Then, the results of the RAG queries are fused using an LLM power context fusion engine, and finally, the fused prompt is processed by an LLM using a response template to produce the final response.

See Figure 2 for an illustration of the APH parallel engine and the context fusion engine.

[--Figure 2: APH Parallel and Context Fusion Engines--]  
*Note: The diagram illustrates the structure of APH parallel and context fusion engines.*

## MRCA Architecture Component

MRCA Microservice BFF’s frontend and backend APIs are implemented using FastAPI. The frontend service is a web interface built with Streamlit. The interface files are located in the `frontend` directory, which is defined as a Python package (`__init__.py`). The core file of the interface is `bot.py`, which hosts the section manager functionality, handles persistent conversation history, displays chat conversation, and captures the user's prompts.

The backend service files are located in the `backend` directory, which is also defined as a Python package. The `main.py` file is the core component of the backend interface. It orchestrates the entire APH process, see Figure 1 and Figure 2. Additionally, to construct the database, the system uses a set of standalone Python executable scripts, `cfr_downloader.py` to download the Title 30 CFR PDF files from govinfo.gov, and `build_hybrid_store.py` to build the Neo4j AuraDB database.

Google Gemini 2.5 Pro is used to construct the knowledge graph, and Google `embedding-001` is used to build the vector index. 

See Table A.1 in the Appendix section of this paper for a detailed list of the project codebase structure, including directories, files, classes, and functions. 

## Conclusion

The MRCA Microservice BFF architecture provides modular cohesion and low coupling through frontend and backend service separation, allowing MRCA to be a scalable, maintainable, resilient system. Additionally, MRCA Advanced Parallel HybridRAG (HPA) is a novel approach to RAG that differs from traditional sequential RAG systems by using both VectorRAG and GraphRAG in parallel and fusing their query results. This provides the LLM with more accurate and reliable data based on the fused results of a semantic search and a transversal search of a KG database, which significantly reduces the LLM's hallucinations.

The Hybrid Template System serves as the critical final component that transforms this sophisticated retrieval and fusion capability into practical, regulatory-focused responses. Through its five specialized templates and advanced prompt engineering features, the system ensures that the innovations of the Advanced Parallel Hybrid approach are effectively translated into professional-grade mining regulatory compliance assistance.

Finally, the overall MRCA architecture meets all the quality attributes that should drive any architectural decision-making mentioned by Keeling (2017), such as modifiability, testability, availability, performance, and security.

---

## References

Abdelfattah, A., & Cerny, T. (2023). Filling the gaps in microservice frontend communication: Case for new frontend patterns. *In Proceedings of the 13th International Conference on Cloud Computing and Services Science (CLOSER 2023)*, 1, 184–193. SciTePress. https://doi.org/10.5220/0011812500003488

Keeling, M. (2017). Chapter 5: Dig for architecturally significant requirements. *Design it! From programmer to software architect*. Pragmatic Bookshelf. ISBN-13: 978-1-680-50209-1

Sarmah, B., Patel, S., Hall, B., Pasquali, S., Rao, R., & Mehta, D. (2024, August 9). *HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction*. arXiv. https://arxiv.org/abs/2408.04948

---

## Appendix

### Table A.1  
**MRCA Codebase Structure Table**

| File | Description | Components (Functions & Classes) |
|------|-------------|----------------------------------|
| **Root** |||
| `build_hybrid_store.py` | Knowledge graph and vector index building script using Gemini 2.5 Pro | Classes: `GraphBuilder`, Functions: `main()` |
| `cfr_downloader.py` | Downloads Title 30 CFR PDFs from govinfo.gov | Classes: `CFRDownloader`, Functions: `main()` |
| `docker-compose.yml` | Multi-service container for frontend/backend | Configuration file |
| **frontend/** |||
| `__init__.py` | Frontend package | Package documentation |
| `bot.py` | Main Streamlit chat interface - configuration | Functions: `get_session_id()`, `write_message()`, `display_header()`, `display_disclaimer()`, `display_sidebar()`, `get_welcome_message()`, `call_parallel_hybrid_api()`, `handle_submit()`, `initialize_session()`, `main()` |
| `requirements.txt` | Frontend dependencies (Streamlit, requests, etc.) | Dependencies file |
| `Dockerfile.frontend` | Container configuration for Streamlit frontend service | Docker configuration |
| **frontend/.streamlit/** |||
| `config.toml` | Streamlit theme and UI configuration settings | |
| `secrets.toml` | Frontend secrets and API keys (git-ignored) | |
| **backend/** |||
| `__init__.py` | Backend package | Package documentation + exports |
| `main.py` | FastAPI server, orchestrates Advanced Parallel Hybrid processes | Classes: `ParallelHybridRequest`, `ParallelHybridResponse`, `HealthResponse`, Functions: FastAPI endpoints |
| `parallel_hybrid.py` | Core parallel engine component for VectorRAG + GraphRAG | Classes: `RetrievalResult`, `ParallelRetrievalResponse`, `ParallelRetrievalEngine`, Functions: `get_parallel_engine()` |
| `context_fusion.py` | Core fusion engine - fusion algorithm(s) | Classes: `HybridContextFusion`, Functions: `get_fusion_engine()` |
| `hybrid_templates.py` | Prompt template(s) used to create the final response | Classes: `HybridPromptTemplate`, Functions: `get_template_engine()`, `create_hybrid_prompt()` |
| `config.py` | Pydantic-based configuration management | Classes: `BackendConfig`, Functions: `init_config()`, `get_config()`, `validate_config()`, `get_database_config()`, `get_llm_config()`, `get_logging_config()` |
| `llm.py` | OpenAI GPT-4o and Gemini embeddings | Classes: `LazyLLM`, `LazyEmbeddings`, Functions: `validate_openai_config()`, `get_llm()`, `validate_gemini_config()`, `get_embeddings()` |
| `graph.py` | Neo4j database connection and utilities | Classes: `LazyGraph`, Functions: `validate_neo4j_config()`, `get_graph()`, `get_graph_schema()`, `test_connection()` |
| `utils.py` | Backend utility functions for sessions and formatting | Functions: `get_session_id()`, `get_session_data()`, `save_message()`, `format_regulatory_response()` |
| `requirements.txt` | Backend dependencies (FastAPI, LangChain, Neo4j, etc.) | Dependencies file |
| `Dockerfile.backend` | Container configuration for FastAPI backend service | Docker configuration |
| **backend/tools/** |||
| `__init__.py` | Tools package documentation for MSHA regulatory queries | Package documentation |
| `vector.py` | VectorRAG tool for semantic search | Functions: `get_neo4j_vector()`, `get_vector_retriever()`, `create_vector_chain()`, `search_regulations_semantic()`, `search_regulations_detailed()`, `get_vector_tool()` |
| `cypher.py` | GraphRAG tool for Cypher query generation and graph traversal | Functions: `get_cypher_qa()`, `query_regulations()`, `query_regulations_detailed()`, `get_cypher_tool()` |
| `general.py` | General MSHA tool for fallback and overview responses | Functions: `create_msha_general_chat()`, `provide_msha_guidance()`, `provide_regulatory_overview()`, `handle_out_of_scope_questions()`, `get_general_tool()`, `get_overview_tool()`, `create_general_chat_chain()`, `test_general_tool()`, `create_general_chat_tool()` |

*Note: The table illustrates a detailed list of the MRCA codebase structure, including a short description of each MRCA file.*

---
---

# Module 4 Capstone Milestone: Software Project Plan

---

## Module 4 Capstone Milestone: Software Project Plan

The Mining Regulatory Compliance Assistant (MRCA), as stated in the previous Module 3 - Software Design section of this project, “will provide a quick, reliable, and easy way to query Mine Safety and Health Administration (MSHA) regulations using natural language” (Ricciardi, 2025). However, after the integration of the novel Advanced Parallel HybridRAG (APH) within the application’s Microservice Backends-for-Frontends (BFF) architecture, in addition to providing MSHA regulations queries, the application will also serve as a test and research tool for APH.

To that end, new features were added to the MRCA design to support testing and research, including a circuit breaker for system stability, a system health monitor, various fusion algorithms, various final prompt templates, and a response metric evaluator. To illustrate the MRCA architecture core components, this document provides a UML backend class diagram, a frontend components diagram, and a UML state machine diagram of the MRCA system core components.

---

## MRCA Architecture Overview

Used as a reference from the Module 3 - Software Design section of this project, the following diagram illustrates MRCA’s architecture. It illustrates the application’s microservice architecture, core components’ data/control flow, and related files. The system leverages an HTTP RESTful API built using FastAPI to create two micro-services. The micro-service frontend is built using Streamlit as a web User Interface (UI), and the micro-service backend leverages the APH system for retrieval and an LLM for prompt processing.

Note that this diagram does not illustrate the new features adopted in the last development iteration, as well as the unloading of the MSHA data from the govinfo.gov MRCA component, and the Knowledge Graph (KG) database builder MRCA component.

[--Figure 1: MRCA Architecture Diagram--]

---

## Frontend Components

The MRCA frontend does not include classes, as the application is built in Python. Unlike Java, Python is not a strictly object-oriented programming language; it allows a blend of procedural, functional, and object-oriented programming, and depending on the framework used and requirements, classes are not always the best solution. Thus, the MRCA based on the Streamlit framework does not use classes. MRCA frontend, the web UI micro-service, is coded using a functional programming style.

The following diagram illustrates the frontend core component logic that cross-references to the Front Manager Streamlit UI component of the MRCA Architecture diagram.

[--Figure 2: MRCA Frontend Core Components Diagram--]

### Table 1  
**MRCA Architecture and Frontend Components Cross-references**

| MRCA Architecture Component | MRCA Frontend Module         | Key Functions/Attributes |
|-----------------------------|------------------------------|---------------------------|
| Frontend Service API        | Bot (streamlit_module)       | `main():handle_submit(msg:str)`, `initialize_session()` |
| State & Configuration       | streamlit_state, ui_function | `session_state`, `session_id`, `fusion_strategy` |
| UI Rendering                | ui_function, ui_module       | Header, disclaimer, sidebar, chat |
| API Integration             | http_client, data_processor  | Backend API calls, response processing |
| Utilities                   | utility                      | `get_session_id()`, `get_welcome_message()`, `get_confidence_level()` |

*Note: The table illustrates the frontend core functionality and cross-references to the Frontend Core Components with the MRCA Architecture diagram.*

---

## Backend Class Diagram

The MRCA backend micro-service implements the APH system and FastAPI. The files are located in the `backend` directory, with the `main.py` components orchestrating the entire functionality of the backend. The backend system combines object-oriented and functional programming. It also uses external services through API calls. Services such as OpenAI and Google APIs for LLMs use and Neo4j AuraDB for a graph database.

[--Figure 3: MRCA Backend Class Diagram--]

### Table 2  
**MRCA Architecture Components and Backend Classes Cross-references**

| MRCA Architecture Component | MRCA Backend Classes Cross-Reference |
|-----------------------------|--------------------------------------|
| Frontend Service API        | Not shown (interacts with `main.py`) |
| Backend Service API         | `main.py`, `ParallelHybridResponse` |
| Advanced Parallel HybridRAG | `ParallelRetrievalEngine`, `ContextFusionEngine`, `HybridPromptTemplate` |
| Parallel Engine             | `parallel_hybride.py`, `ParallelRetrievalEngine` class |
| Context Fusion Engine       | `context_fusion.py`, `FusionEngine` class, `FusionStrategy` enum |
| Template System             | `hybride_templates.py`, `HybridPromptTemplate` class, `TemplateType` enum |
| LLMs API                    | `graph.py`, `llm.py`, `LazyGraph`, `LazyLLM`, `LazyEmbeddings` |
| Vector Search               | `vector.py` (functions) |
| Graph Search                | `cypher.py` (functions) |
| Data Layer API              | `database.py`, `EnhancedNeo4jDatabase`, `DatabaseConfig` class |

---

## The Build Data Class Diagram

The built data components are not illustrated in the original MRCA Architecture diagram. However, it is crucial to describe their logic as they play a crucial role. The built data includes two standalone scripts stored in the `build_data` directory.

- `cfr_downloader.py`: Downloads MSHA Title 30 CFR PDFs using the `CFRDownloader` class  
- `build_hybrid_store.py`: Builds the Neo4j KG database with property-indexed vectors using the `HybridStoreBuilder` class.  
  - Uses a Google LMM to generate the KG  
  - Embedding model for vector indexes

[--Figure 4: MRCA Build Data Class Diagram--]

*Note: The diagram illustrates the MRCA building KG with vectors embedding property class and the MSHA regulation data downloading class.*

---

## MRCA Machine State Diagram

The following diagram illustrates the runtime state of different objects related to the architecture components found in the MRCA Architecture diagram and the Frontend Core Components diagram. The objects are based on the class objects found in the MRCA Backend Class diagram.

[--Figure 5: MRCA Machine State Diagram--]

### Table 3  
**MRCA Architecture Components and MRCA Object States Cross-references**

| MRCA Architecture Component | MRCA State Diagram Cross-Reference |
|-----------------------------|------------------------------------|
| Frontend Service API        | MRCA Frontend Object, `st.session_state` (Streamlit) |
| Backend Service API         | MRCA Backend Object (`main.py`) |
| Advanced Parallel HybridRAG | `ParallelRetrievalEngine`, `HybridFusionEngine`, `HybridPromptTemplate` |
| Parallel Engine             | `ParallelRetrievalEngine` Object |
| Context Fusion Engine       | `HybridFusionEngine` Object |
| Template System             | `HybridPromptTemplate` Object |
| LLMs API                    | LLM Invocation states within `HybridPromptTemplate` |
| Vector Search               | Object state in `ParallelRetrievalEngine` |
| Graph Search                | Object state in `ParallelRetrievalEngine` |
| Data Layer API              | `EnhancedNeo4jDatabase` Object (`database.py`) |

*Note: The table cross-references the MRCA Architecture diagram components with the State diagram object states.*

---

## Conclusion

This document provides a detailed class diagram of the MRCA backend, a class diagram of the build data classes, and state machine diagrams illustrating the state of MRCA objects at runtime. The diagrams showcase the functionality, modularity, scalability, maintainability, and resilience of the MRCA system. Specifically, by showcasing the backend classes and objects' state (behavior), the diagrams illustrate well the functionality of the novel APH system found in the backend micro-service of the MRCA architecture.

---

## References

Ricciardi (2025, June 29). *Module 3 Capstone Milestone: Software Design* [Student Essay]. CSC480 Capstone Computer Science. CSU Global.

---
---

# Module 5 Capstone Milestone: Fault-tolerant Software

---

## Module 5 Capstone Milestone: Fault-tolerant Software

As early as 1984, a study by Slivinski et al. (1984) identified software faults as the most significant issue in software systems. Today, designing fault-tolerant software is essential, as software applications have become larger and more complex, and consequently more prone to faults. As a result, fault tolerance is now an integral part of software design, making software systems more reliable and resilient. This paper examines how fault tolerance is implemented in modern software and describes how it is implemented with the Mining Regulatory Compliance Assistant (MRCA) project, within its microservices architecture and Advanced Parallel HybridRAG (APH) system.

---

## Fault-Tolerant Software and Design

Fault-tolerant software is software designed to detect and recover from faults that are happening or have already happened in either the software or hardware (Inacio, 1998). In other words, the primary goal of fault-tolerance systems is to increase a software application's dependability despite internal faults or failures (Solouki et al., 2024). 

On the other hand, fault-tolerant software design is a set of principles, strategies, and architectural patterns used to build software systems that can detect and recover from faults or failures (Andersen, 2024). The primary objective of fault-tolerant software design is to design a reliable and resilient software system. The key fault-tolerant software principles are:

- **Resilience**
- **Redundancy**
- **Error detection and correction**
- **Checkpointing** (periodically saving system state)
- **Continuous operation**  
(Lee, 2025; Gopinath, 1986; GeeksforGeeks, 2024)

The key fault-tolerant software design techniques include:

- Leveraging microservices architecture for improved resilience  
- Using graceful degradation components  
- Adding redundancy via additional components or systems  
- Load balancing across servers  
- Implementing health check mechanisms  
- Using foundation patterns (e.g., publish-subscribe, SOA)  
- Implementing a circuit breaker system to prevent cascading failures  
(ByteByteGo, 2024; Keeling, 2027; Andersen, 2024)

---

## Fault Tolerance in MRCA

MRCA employed various fault-tolerant techniques that are woven into its microservices architecture. 

- A **circuit breaker system** is implemented via the `CircuitBreaker` class in `circuit_breaker.py`, monitoring the health of:
  - Neo4j database connections  
  - OpenAI API calls  
  - Google Gemini API calls  
  It manages failure thresholds, timeouts, and recovery testing.

- A **health monitoring system** is integrated using the FastAPI framework with:
  - `/health` endpoint for overall system status  
  - `parallel_hybrid/health` for APH components  
  - Tool-specific checks for vector, cypher, and general guidance modules  
  - Docker health checks for automatic service restarts  

- A **safe tool getter system** using `get_vector_tool_safe()` and `get_cypher_tool_safe()` provides fallback functions with informative error messages to prevent frontend crashes.

- The **frontend** (Streamlit) maintains **persistent session management**, remembering session state and conversation history even during API failures.

- The frontend API errors are handled through `call_parallel_hybrid_api()` in `frontend/bot.py`.

- **Pydantic** is used to validate data requests and reject malformed input.

- The `ParallelHybridRequest` class in `backend/main.py` validates:
  - User input  
  - Session identifiers  
  - Fusion strategies  
  - Template types  
  This prevents invalid data from entering the APH system.

---

## Conclusion

Fault-Tolerant Software is reliable and resilient software that is designed to withstand faults and failures, whether they are caused by software bugs, hardware malfunctions, or external factors. Such software implements redundancy, error detection and correction, checkpointing, and continuous operation within its architecture and implementation. 

This software is designed using techniques, patterns, and architecture such as microservices, graceful degradation, load balancing, health monitoring, foundational patterns, and circuit breakers. MRCA implements most of these strategies and techniques deep within its design and implementation. In essence, MRCA integrates a fault-tolerance design and techniques from the ground up; fault-tolerance is woven into its microservices architecture and implementation, ensuring that the system is reliable and resilient.

---

## References

Andersen, G. (2024, February 8). *Building resilient systems – A guide to fault-tolerant software architecture*. MoldStud. https://moldstud.com/articles/p-building-resilient-systems-through-fault-tolerant-software-architecture

ByteByteGo. (2024, February 14). *A cheat sheet for designing fault-tolerant systems*. ByteByteGo. https://bytebytego.com/guides/a-cheat-sheet-for-designing-fault-tolerant-systems/

GeeksforGeeks. (2024, June 19). *Basic fault-tolerant software techniques*. https://www.geeksforgeeks.org/software-engineering/basic-fault-tolerant-software-techniques/

Gopinath, D. (1986). *A tutorial on the principles of fault tolerance*. Sādhanā, 11(1–2), 7–22. https://www.ias.ac.in/article/fulltext/sadh/011/01-02/0007-0022

Keeling, M. (2017). Chapter 7: Create a Foundation with Patterns. *Design it! From programmer to software architect*. Pragmatic Bookshelf. ISBN-13: 978-1-680-50209-1

Lee, S. (2025, June 11). *Fault Tolerance 101: A Beginner’s Guide*. Number Analytics. https://www.numberanalytics.com/blog/fault-tolerance-101

Inacio, C. (1998). *Software fault tolerance - Electrical and computer engineering [Course]*. Carnegie Mellon University. https://users.ece.cmu.edu/~koopman/des_s99/sw_fault_tolerance/

Slivinski, T., Broglio, C., Wild, C., Goldberg, J., Levitt, K., Hitt, E., & Webb, J. (1984). *Study of fault-tolerant software technology* (NASA Contractor Report 172385). NASA Langley Research Center. https://ntrs.nasa.gov/api/citations/19870002074/downloads/19870002074.pdf

Solouki, M. A., Angizi, S., & Violante, M. (2024, April 16). *Dependability in embedded systems: A survey of fault tolerance methods and software-based mitigation techniques* (arXiv:2404.10509v1) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2404.10509

---
---

# Module 5 Capstone Milestone: Fault-tolerant Software

---

## Fault-tolerant Software

As early as 1984, a study by Slivinski et al. (1984) identified software faults as the most significant issue in software systems. Today, designing fault-tolerant software is essential, as software applications have become larger and more complex, and consequently more prone to faults. As a result, fault tolerance is now an integral part of software design, making software systems more reliable and resilient. This paper examines how fault tolerance is implemented in modern software and describes how it is implemented with the Mining Regulatory Compliance Assistant (MRCA) project, within its microservices architecture and Advanced Parallel HybridRAG (APH) system.

---

## Fault-Tolerant Software and Design

Fault-tolerant software is software designed to detect and recover from faults that are happening or have already happened in either the software or hardware (Inacio, 1998). In other words, the primary goal of fault-tolerance systems is to increase a software application's dependability despite internal faults or failures (Solouki et al., 2024). On the other hand, fault-tolerant software design is a set of principles, strategies, and architectural patterns used to build software systems that can detect and recover from faults or failures (Andersen, 2024). The primary objective of fault-tolerant software design is to design a reliable and resilient software system.

The key fault-tolerant software principles are:

* Resilience
* Redundancy
* Error detection and correction
* Checkpointing (periodically saving system state)
* Continuous operation (Lee, 2025; Gopinath, 1986; GeeksforGeeks, 2024)

The key fault-tolerant software design techniques include:

* Leveraging microservices architecture for improved resilience
* Using graceful degradation components for continuous operation after faults or failures
* Adding redundancy by having additional components or systems that can take over in case of a failure
* Load balancing for distributing incoming network traffic across multiple servers
* Implementing health check mechanisms for crucial components
* Using foundation patterns such as publish-subscribe or service-oriented architecture to promote testing and interoperability
* Implementing a circuit breaker system to prevent cascading failures (ByteByteGo, 2024; Keeling, 2027; Andersen, 2024)

---

## Fault Tolerance in MRCA

MRCA employed various fault-tolerant techniques that are woven into its microservices architecture.

* A **circuit breaker system** is implemented through the `CircuitBreaker` class in the `circuit_breaker.py` module. It monitors external dependencies like Neo4j database connections, OpenAI API calls, and Google Gemini API calls. It handles failure thresholds, timeouts, and recovery testing.

* MRCA has an **integrated health monitoring system** using the FastAPI framework. It provides:

  * Basic health checks: `/health`
  * Component-specific checks: `parallel_hybrid/health`
  * Dedicated RAG tool checks (vector search, cypher queries, general guidance)
  * Docker container health checks with auto-restart functionality

* A **safe tool getter system** ensures continuity when a primary RAG tool fails:

  * `get_vector_tool_safe()` and `get_cypher_tool_safe()` return fallback functions with informative error messages rather than crashing.

* The **frontend**, built with Streamlit, implements:

  * Persistent session management to remember history and settings even on API failure
  * API error handling via `call_parallel_hybrid_api()` in `frontend/bot.py`

* **Pydantic** is used to validate and reject malformed requests.

* The `ParallelHybridRequest` class in `backend/main.py` validates:

  * User inputs
  * Session identifiers
  * Fusion strategies
  * Template types

This prevents invalid data from propagating through and being used by the APH system.

---

## Conclusion

Fault-tolerant software is reliable and resilient software designed to withstand faults and failures, whether caused by bugs, hardware issues, or external disruptions. It integrates redundancy, error detection and correction, checkpointing, and continuous operation through architectural strategies like microservices, graceful degradation, load balancing, health monitoring, and circuit breakers.

MRCA embodies these strategies in its design and implementation. Fault tolerance is foundational to MRCA, making the system dependable and robust by design.

---

## References

* Andersen, G. (2024, February 8). *Building resilient systems – A guide to fault-tolerant software architecture*. MoldStud. [https://moldstud.com/articles/p-building-resilient-systems-through-fault-tolerant-software-architecture](https://moldstud.com/articles/p-building-resilient-systems-through-fault-tolerant-software-architecture)

* ByteByteGo. (2024, February 14). *A cheat sheet for designing fault-tolerant systems*. ByteByteGo. [https://bytebytego.com/guides/a-cheat-sheet-for-designing-fault-tolerant-systems/](https://bytebytego.com/guides/a-cheat-sheet-for-designing-fault-tolerant-systems/)

* GeeksforGeeks. (2024, June 19). *Basic fault-tolerant software techniques*. [https://www.geeksforgeeks.org/software-engineering/basic-fault-tolerant-software-techniques/](https://www.geeksforgeeks.org/software-engineering/basic-fault-tolerant-software-techniques/)

* Gopinath, D. (1986). *A tutorial on the principles of fault tolerance*. *Sādhanā, 11*(1–2), 7–22. [https://www.ias.ac.in/article/fulltext/sadh/011/01-02/0007-0022](https://www.ias.ac.in/article/fulltext/sadh/011/01-02/0007-0022)

* Keeling, M. (2017). *Design it! From programmer to software architect.* Pragmatic Bookshelf. ISBN-13: 978-1-680-50209-1

* Lee, S. (2025, June 11). *Fault Tolerance 101: A Beginner’s Guide*. Number Analytics. [https://www.numberanalytics.com/blog/fault-tolerance-101](https://www.numberanalytics.com/blog/fault-tolerance-101)

* Inacio, C. (1998). *Software fault tolerance - Electrical and computer engineering \[Course]*. Carnegie Mellon University. [https://users.ece.cmu.edu/\~koopman/des\_s99/sw\_fault\_tolerance/](https://users.ece.cmu.edu/~koopman/des_s99/sw_fault_tolerance/)

* Slivinski, T., Broglio, C., Wild, C., Goldberg, J., Levitt, K., Hitt, E., & Webb, J. (1984). *Study of fault-tolerant software technology (NASA Contractor Report 172385)*. NASA Langley Research Center. [https://ntrs.nasa.gov/api/citations/19870002074/downloads/19870002074.pdf](https://ntrs.nasa.gov/api/citations/19870002074/downloads/19870002074.pdf)

* Solouki, M. A., Angizi, S., & Violante, M. (2024, April 16). *Dependability in embedded systems: A survey of fault tolerance methods and software-based mitigation techniques* (arXiv:2404.10509v1) \[Preprint]. arXiv. [https://doi.org/10.48550/arXiv.2404.10509](https://doi.org/10.48550/arXiv.2404.10509)

# Module 6 Capstone Milestone: Software Project Testing Plan&#x20;

**Alexander Ricciardi**
Colorado State University Global
CSC480: Capstone Computer Science
Dr. Shaher Daoud
July 20, 2025

---

## Introduction&#x20;

In software development, *software testing* is a crucial activity in the project‑development lifecycle. It evaluates and improves software systems, ensuring they function correctly, remain secure, satisfy stakeholders’ requirements, and deliver value to end‑users. The Mining Regulatory Compliance Assistant (MRCA) is an AI‑powered system that employs **Advanced Parallel HybridRAG (APH)**—a novel retrieval‑augmented generation (RAG) technique that fuses vector similarity search, graph‑based traversal, and semantic fusion—to provide grounded answers about U.S. MSHA regulations (30 CFR). This AI architecture introduces challenges such as non‑deterministic outputs, data‑dependency factors, and hallucination risks; consequently, a comprehensive testing strategy is essential.

## Architecturally Significant Requirements (ASRs)&#x20;

To design and execute effective test cases, MRCA’s **ASRs** must be clear. Chief among them is reliability in retrieving and generating regulations, measured by:

* **Retrieval confidence scores** for vector and graph results
* **Fusion‑quality scores** for merged search results
* **Final confidence scores** for aggregated outputs

These metrics can draw on recent RAG‑evaluation research such as HyPA‑RAG, RA‑RAG, and Auepora‑style evaluators, which provide domain‑relevance scoring, reliability‑aware weighting, and unified confidence assessments.

## Testing Strategies Overview&#x20;

Following the principle **“test early, test often”**, MRCA adopts a blended **white‑box/black‑box** regimen across five levels:

1. **Unit tests** – CFR parsing, query normalization, embeddings, graph traversals, fusion
2. **Component‑integration tests** – VectorRAG, GraphRAG, and fusion context validity
3. **End‑to‑end tests** – UI and API flows, focusing on performance, reliability, and user value
4. **Reliability & fault‑injection tests** – Simulated outages, latency spikes, and auth failures to validate circuit‑breaker logic and user messaging
5. **Architecture evaluation** – Scoring ASRs to surface design feedback and improvement areas

## Use Test Cases

### Test Case 1 – Regulatory Citation Retrieval (Component Integration)&#x20;

*Input:* “What does **30 CFR 56.12016** say about grounding of electrical equipment?”
*Expected:* Correct CFR section with source; confidence ≥ 0.85 when vector + graph concur; p95 latency ≤ 5 s.
*Failure:* Malformed citation or missing section.

### Test Case 2 – Multi‑Domain Query (Component Integration)&#x20;

*Input:* “What are the regulations for underground drilling generating silica dust near diesel equipment?”
*Expected:* Cites multiple relevant CFR sections; **fusion\_quality** ≥ 0.70.
*Failure:* Missing domain/section, conflicting passages, or low fusion score.

### Test Case 3 – Reliability Under Degraded Services (End‑to‑End)&#x20;

*Scenario:* Simulate Neo4j downtime, slow LLM completion, lost Internet, or expired API key.
*Expected:* Circuit breaker opens, retries/back‑offs engage, user informed, session preserved.
*Failure:* Undetected fault, unhandled exception, or lost session state.

### Test Case 4 – Reliability & Fault‑Injection (Load + Unit)&#x20;

*Scenario:* Concurrent‑load testing with injected faults.
*Expected:* Response time 10–35 s (LLM‑bounded) with correct CFR citations under load.
*Failure:* Excessive latency, incorrect citations, or unhandled faults.

### Test Case 5 – Confidence Score & Hallucination (Architecture Evaluation)&#x20;

*Input:* Off‑domain prompt “What sound does a dog make?”
*Expected:* Pre‑made message explaining off‑domain query handling; in‑domain queries answered with high final confidence.
*Failure:* Low confidence score or hallucinated off‑domain answer.

## Conclusion&#x20;

By uniting traditional software‑testing methods with RAG‑specific evaluations, this plan strengthens MRCA’s reliability, accuracy, robustness, and user value. Early and layered testing—spanning unit to architecture level—targets key ASRs, validates performance under stress, and ensures graceful degradation during failures.

## References&#x20;

* CSU Global. (2025). *Module 6: Project testing* \[Interactive Lecture].
* Hwang, J., Park, J., Park, H., Park, S., & Ok, J. (2024). *Retrieval‑augmented generation with estimation of source reliability* (arXiv:2410.22954).
* IEEE Computer Society. (n.d.). *The importance of software testing*.
* Kalra, R. et al. (2025). *HyPARAG: A hybrid parameter adaptive retrieval‑augmented generation system for AI legal and policy applications* (arXiv:2409.09046 v2).
* Keeling, M. (2017). *Design It! From Programmer to Software Architect* (Chap. 12).
* Yu, H. et al. (2024). *Evaluation of retrieval‑augmented generation: A survey* (arXiv:2405.07437 v2).

---
---

# Module 6 Capstone Milestone: Software Project Testing Plan

---

## Module 6 Capstone Milestone: Software Project Testing Plan

In software development, software testing is a crucial activity of a project development lifecycle that aims to evaluate and improve software systems (IEEE Computer Society, n.d.). It ensures that these systems function correctly, are secure, meet stakeholders’ requirements, and provide value to end users. Many types of software testing methodologies are available to developers, each with different advantages and disadvantages.

The Mining Regulatory Compliance Assistant (MRCA) is an AI-powered system that uses a novel RAG technique, Advanced Parallel HybridRAG (APH), that combines vector similarity search, graph-based traversal search, and intelligent semantic fusion to provide grounded and accurate answers about U.S. Mine Safety & Health Administration (MSHA) regulations (30 CFR). This combination of AI and novel RAG system adds testing challenges to traditional software testing, such as non-deterministic outputs, AI data dependency factors, and the risk of AI hallucinations.

This paper describes a testing strategy for the MRCA, including unit, integration, end-to-end for UI/API, reliability/fault-injection, and overall architectural evaluation testing, focusing on Architecturally Significant Requirements (ASRs) of the project, and provides five use test cases based on these testing strategies.

---

## Architecturally Significant Requirements

To effectively design and execute test cases for a software project, it is important to understand its Architecturally Significant Requirements (Keeling, 2017). For MRCA, this translates to ensuring that the system is reliable in retrieving and generating MSHA regulations by implementing evaluation metrics such as retrieval confidence scores for vector and graph results, search results fusion quality scores, and final confidence scores for the aggregated outputs.

These evaluation scores can be based on or similar to approaches such as:

- Hybrid Parameter-Adaptive RAG (HyPA-RAG) that score each retrieved passage for domain relevance in the legal field called signals that can be defined as identifiers, terms, and numeric thresholds (Kalra et al., 2025)
- Reliability‑Aware RAG (RA-RAG) scoring proposed by Hwang et al. (2024)
- Auepora (A Unified Evaluation Process of RAG) RAG evaluation metric proposed by Ya et al. (2024)

---

## Testing Strategies Overview

One of the most important testing principles is to test early, test often, mix white‑box and black‑box, and escalate from quick checks to targeted and deep evaluations (CSU Global, 2025). 

A white‑box is a test that has explicit knowledge of the internal structure and implementation details of the software; on the other hand, a black‑box is a test that does not have explicit knowledge of the internal structure and implementation details of the software.

MRCA uses five test levels, which are a combination of white‑box and black‑box tests that focus on its ASRs:

- **Unit Tests** for CFR parsing, query normalization, embedding calls, graph traversals, and fusion
- **Component integration tests** for context validity for VectorRAG, GraphRAG, and fusion, to evaluate the accuracy and confidence of the generated results
- **End‑to‑end testing** for UI and API flows, measuring performance, reliability, and user value
- **Reliability and fault‑injection testing** to simulate service outages, latency, and auth failures to test the circuit breaker system and user messaging
- **Overall architecture evaluation** to score ASRs with the goal of collecting feedback and identifying areas needing improvement

---

## Use Test Cases

### Test Case 1: Regulatory Citation Retrieval - Component Integration Test

Confirm that MRCA returns the correct CFR citation results with reasonable confidence scores and latency.

**Example of input**:  
“What does 30 CFR 56.12016 say about grounding of electrical equipment?”

**Expected Output**:  
Correct CFR result with source; confidence ≥ 0.85 when vector+graph agree; p95 latency ≤ 5s.  
**Failure condition**: Malformed citation and section missing.

---

### Test Case 2: Multi-Domains Query - Component Integration Test

Test the fusion validity across multiple regulatory domains, such as dust control, ventilation, and respirators.

**Example of input**:  
“What are the regulations for underground drilling generating silica dust near diesel equipment?”

**Expected Output**:  
Cite multiple CFR sections with fusion_quality score ≥ 0.70.  
**Failure condition**: Missing section/domain, conflicting passages, low complementarity (low fusion score).

---

### Test Case 3: Reliability Under Degraded External Services - End-to-End Testing

Tests the circuit breaker functionality under various fault scenarios.

**Example of condition**:  
Simulate Neo4j DB downtime, slow LLM completion, no internet, expired API key.

**Expected Output**:  
Circuit breaker triggers open state, user is informed, session is preserved, system retries affected process.

---

### Test Case 4: Reliability, Fault-Injection Test, and Unit Tests

Test system performance and fault handling under load and fault conditions.

**Expected Output**:  
Response time within 10–35s, accurate CFR citations, based on load and concurrency testing metrics.

---

### Test Case 5: Confidence Score and Hallucination – Overall Architecture Evaluation (AHP)

Test if the system detects unsupported/off-domain prompts and assigns correct confidence levels.

**Example input**:  
“What sound a dog makes?”

**Expected Output**:  
Predefined response indicating off-domain question.  
**Failure condition**: Incorrect response, low confidence, or irrelevant reply.

---

## Conclusion

MRCA is a complex system that combines AI and a novel RAG system, adding testing challenges to traditional software testing. This document provided a testing plan for MRCA, addressing its novel APH technology by implementing traditional and RAG/generative AI testing techniques that include unit testing, integration testing, end-to-end testing for UI/API, reliability testing for fault tolerance, and architectural evaluations based on ASRs.

The provided use test cases map to these test types, showcase specific inputs and expected results, and test regulatory responses, system performance under heavy load, and resilience to failure. Through these testing techniques, MRCA can be improved and become a more reliable, accurate, robust, and valuable tool for querying MSHA regulations.

---

## References

- CSU Global (2025). *Module 6: Project testing* [Interactive Lecture]. Canvas. https://csuglobal.instructure.com/courses/110425/pages/module-6-overview?module_item_id=5733358
- Hwang, J., Park, J., Park, H., Park, S., & Ok, J. (2024, June 2). *Retrieval-augmented generation with estimation of source reliability* (arXiv:2410.22954) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2410.22954
- IEEE Computer Society. (n.d.). *The importance of software testing*. IEEE Computer Society. https://www.computer.org/resources/importance-of-software-testing
- Kalra, R., Wu, Z., Gulley, A., Hilliard, A., Guan, X., Koshiyama, A., & Treleaven, P. (2025, February 25). *HyPARAG: A hybrid parameter adaptive retrieval-augmented generation system for AI legal and policy applications* (arXiv No. 2409.09046v2) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2409.09046
- Keeling, M. (2017). Chapter 12: Give the architecture a report Card. *Design it! From programmer to software architect*. Pragmatic Bookshelf. ISBN-13: 978-1-680-50209-1
- Yu, H., Gan, A., Zhang, K., Tong, S., Liu, Q., & Liu, Z. (2024, July 3). *Evaluation of retrieval-augmented generation: A survey* (arXiv No. 2405.07437v2) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2405.07437

---
---

© 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System

---

