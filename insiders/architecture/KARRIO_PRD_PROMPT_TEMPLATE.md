# Advanced Karrio PRD Generation Prompt Template

## 🎯 **Template Purpose**

This template provides a comprehensive framework for generating detailed Product Requirements Documents (PRDs) and Implementation Specifications for Karrio features. It follows the established patterns from successful Karrio PRDs and ensures consistency, thoroughness, and technical depth.

## 📋 **PRD Generation Prompt Template**

### **Core Prompt Structure**

```
You are tasked with creating a comprehensive Product Requirements Document (PRD) for [FEATURE_NAME] in the Karrio shipping platform. This PRD should serve as a complete technical specification that enables developers, AI agents, and stakeholders to understand, implement, maintain, and extend the feature.

## Context and Requirements

**Feature Name**: [FEATURE_NAME]
**Feature Category**: [API/Backend/Frontend/Integration/Engine/Automation]
**Target Users**: [Developers/End Users/Partners/Administrators]
**Business Objective**: [Primary business goal this feature serves]
**Technical Complexity**: [Low/Medium/High/Complex]
**Integration Points**: [List of systems this feature interacts with]

## Required Document Structure

Create a PRD following this exact structure:

### 1. Executive Summary (🎯)
- **Purpose**: Clear business objective and value proposition
- **Scope**: What is included and excluded from this feature
- **Success Metrics**: Measurable outcomes and KPIs
- **Timeline**: High-level implementation phases

### 2. Architecture Overview (🏗️)
- **System Architecture Diagram**: Mermaid diagram showing how the feature fits into Karrio
- **Component Integration**: How it connects with existing systems
- **Data Flow**: High-level data movement and processing
- **Dependency Map**: Required and optional dependencies

### 3. Technical Specification (📊)
- **Data Models**: Complete model definitions with relationships
- **API Schema**: GraphQL types, inputs, and mutations
- **Business Logic**: Core algorithms and processing logic
- **Security Considerations**: Authentication, authorization, validation

### 4. Implementation Details (🔧)
- **Core Components**: Detailed technical implementation
- **Processing Pipeline**: Step-by-step execution flow
- **Error Handling**: Comprehensive error scenarios and responses
- **Performance Considerations**: Scalability and optimization requirements

### 5. API Integration (🌐)
- **GraphQL Schema**: Complete schema definitions
- **REST Endpoints**: Any REST API surfaces
- **Request/Response Examples**: Actual JSON examples
- **Authentication Flow**: How API access is secured

### 6. Data Flow Diagrams (🔄)
- **Primary Use Case Flow**: Main user journey as Mermaid sequence diagram
- **Error Flow**: How errors are handled and propagated
- **Integration Flow**: How external systems interact
- **Processing Pipeline**: Internal data transformation flow

### 7. Current Implementation Status (✅❌)
- **What's Implemented**: Detailed inventory of working features
- **Current Limitations**: Technical and functional constraints
- **Known Issues**: Bugs, performance problems, missing features
- **Dependencies**: What needs to be built first

### 8. Testing Strategy (🧪)
- **Unit Testing**: Core logic and model testing
- **Integration Testing**: API and system integration tests
- **End-to-End Testing**: Complete user workflow testing
- **Performance Testing**: Load and stress testing requirements

### 9. Future Roadmap (🔮)
- **Phase 1**: Immediate improvements and fixes
- **Phase 2**: Major enhancements and new capabilities
- **Phase 3**: Advanced features and optimization
- **Long-term Vision**: Strategic direction and possibilities

### 10. Implementation Examples (📚)
- **Basic Usage**: Simple, common use cases
- **Advanced Usage**: Complex scenarios and edge cases
- **Integration Examples**: How to integrate with external systems
- **Configuration Examples**: Setup and customization options

### 11. Developer Guide (🔧)
- **Setup Instructions**: How to enable and configure the feature
- **Development Workflow**: How to build and test changes
- **Debugging Guide**: How to troubleshoot issues
- **Extension Points**: How to customize and extend functionality

## Required Diagram Types

Include these specific Mermaid diagrams:

1. **System Architecture**: How the feature fits into Karrio's overall architecture
2. **Component Diagram**: Internal component relationships and dependencies
3. **Sequence Diagram**: Primary user interaction flow
4. **Data Flow Diagram**: How data moves through the system
5. **State Diagram**: If applicable, state transitions and lifecycle
6. **Entity Relationship**: Database schema and relationships

## Technical Depth Requirements

**Code Examples**: Include actual Python, TypeScript, and GraphQL code snippets
**Configuration**: Show actual configuration files and settings
**API Examples**: Provide complete curl commands and responses
**Error Scenarios**: Document specific error conditions and responses
**Performance Metrics**: Include benchmarks, targets, and monitoring

## Quality Standards

**Accuracy**: All code and examples must be syntactically correct
**Completeness**: Cover all major use cases and edge cases
**Clarity**: Write for both technical and non-technical stakeholders
**Actionability**: Provide enough detail for immediate implementation
**Maintainability**: Structure for easy updates and revisions

## Feature-Specific Context

[Provide specific context about the feature you're documenting, including:]
- Current codebase location and structure
- Existing related features and their implementations
- User stories and business requirements
- Technical constraints and architectural decisions
- Integration requirements with external systems
```

## 🎯 **Specialized Prompt Variations**

### **For Backend Features**

```
Additionally focus on:
- Database schema design and migrations
- Service layer architecture and patterns
- Background job processing and queuing
- Caching strategies and data consistency
- API performance and optimization
- Security and data protection measures
```

### **For Frontend Features**

```
Additionally focus on:
- Component architecture and reusability
- State management and data flow
- User experience and accessibility
- Performance optimization and lazy loading
- Error handling and user feedback
- Responsive design and mobile support
```

### **For Integration Features**

```
Additionally focus on:
- External API integration patterns
- Authentication and authorization flows
- Error handling and retry mechanisms
- Rate limiting and throttling
- Webhook handling and security
- Monitoring and observability
```

### **For Engine/Algorithm Features**

```
Additionally focus on:
- Algorithm design and complexity analysis
- Performance benchmarking and optimization
- Edge case handling and validation
- Scalability and resource management
- Testing strategies for complex logic
- Configuration and tuning parameters
```

## 📊 **Evaluation Criteria**

Rate the generated PRD on these dimensions (1-10 scale):

1. **Technical Accuracy**: Code examples work and schemas are valid
2. **Completeness**: All required sections covered thoroughly
3. **Clarity**: Easy to understand for target audience
4. **Actionability**: Provides enough detail for implementation
5. **Visual Quality**: Diagrams enhance understanding
6. **Integration Awareness**: Shows how feature fits into Karrio ecosystem
7. **Security Consciousness**: Addresses security considerations appropriately
8. **Performance Awareness**: Considers scalability and optimization
9. **Error Handling**: Comprehensive error scenarios covered
10. **Future-Proofing**: Extensible design that can evolve

**Target Score**: 8.5+ for production-ready PRDs

## 🔄 **Iterative Improvement Process**

1. **Initial Draft**: Generate complete PRD following template
2. **Technical Review**: Validate code examples and architecture
3. **Stakeholder Review**: Ensure business requirements are met
4. **Developer Review**: Verify implementability and completeness
5. **Final Polish**: Refine diagrams, examples, and formatting

## 📝 **Sample Usage**

```
I need a PRD for implementing "Real-time Shipment Tracking with Webhooks" in Karrio.

Feature Context:
- Integration with multiple carrier APIs for tracking updates
- Real-time notifications to customers and internal systems
- Webhook system for external integrations
- Dashboard UI for tracking visualization
- Background job processing for polling carriers

Current State:
- Basic tracking exists but is polling-based
- No real-time updates or webhook system
- Limited carrier support for push notifications
- Manual refresh required in dashboard

Business Goals:
- Reduce customer service inquiries about shipment status
- Enable real-time integrations with customer systems
- Improve user experience with live updates
- Support proactive delivery management

Generate a comprehensive PRD following the template above.
```

## 🛠️ **Implementation Notes**

**For AI Agents**: This template provides structured guidance for generating consistent, high-quality PRDs that match Karrio's established patterns and quality standards.

**For Human Developers**: Use this template as a checklist when creating new feature specifications to ensure completeness and consistency.

**For Code Reviews**: Reference this template when reviewing PRDs to ensure they meet Karrio's documentation standards.

**For Stakeholders**: This template ensures all PRDs contain the information needed for technical and business decision-making.

## 🔗 **Reference Examples**

Use these existing Karrio PRDs as reference implementations:

1. **KARRIO_SHIPPING_RULES_PRD.md**: Engine/algorithm feature example
2. **KARRIO_APPS_ARCHITECTURE.md**: Platform architecture example
3. **KARRIO_OAUTH_INTEGRATION_PRD.md**: Security/authentication example
4. **KARRIO_WORKFLOW_PRD.md**: Complex backend system example

Each reference demonstrates different aspects of the template applied to real Karrio features.
