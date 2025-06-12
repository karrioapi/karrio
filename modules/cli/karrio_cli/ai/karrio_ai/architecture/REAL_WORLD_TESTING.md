# Real-World Carrier Integration Testing Guide

This guide shows you how to test the Karrio ADK agent with **real carrier integrations** using various input formats that you encounter in practice.

## 🎯 What the Agent Can Handle

The ADK agent can build complete carrier integrations from:

### ✅ **OpenAPI/Swagger Specifications**
- JSON or YAML format
- Full endpoint definitions
- Authentication schemes
- Request/response schemas

### ✅ **Website URLs for API Documentation**
- Automatic content scraping
- Endpoint extraction
- Code example parsing
- Link following for related docs

### ✅ **PDF Documentation Files**
- Text extraction from PDFs
- Table parsing
- API endpoint detection
- Code example extraction

### ✅ **Raw Text Documentation**
- Markdown files
- Plain text docs
- API reference materials
- Mixed content formats

## 🚀 Quick Start for Real-World Testing

### 1. **Environment Setup**

```bash
# Activate development environment
source ./bin/activate-env

# Set up environment
cd modules/cli/karrio_cli/ai
cp .env.sample .env
# Edit .env and add your Google API key
```

### 2. **Start the ADK Web Interface**

```bash
# From karrio root directory
python -m karrio_cli agent web
```

Open `http://localhost:8080` in your browser.

## 📋 Testing Scenarios

### **Scenario 1: OpenAPI Specification Integration**

**Input**: You have an OpenAPI spec file from a carrier.

**Conversation with Agent**:
```
I have an OpenAPI specification for a new carrier called "FastShip".
Here's their API spec:

[Paste the entire OpenAPI JSON/YAML content]

Please analyze this and build a complete Karrio integration.
```

**Expected Output**:
- ✅ API endpoint analysis
- ✅ Authentication method detection
- ✅ Schema generation from OpenAPI models
- ✅ Complete integration with mappings and tests

### **Scenario 2: Website URL Documentation**

**Input**: You only have a URL to the carrier's API docs.

**Conversation with Agent**:
```
I need to build an integration for "RegionalExpress" carrier.
Their API documentation is at: https://developer.regionalexpress.com/api

Can you scrape their documentation and build a complete integration?
Include rate calculation, shipment creation, and tracking.
```

**Expected Output**:
- ✅ Automatic website scraping
- ✅ Content extraction and analysis
- ✅ API endpoint identification
- ✅ Integration generation based on scraped content

### **Scenario 3: PDF Documentation**

**Input**: You have a PDF file with API documentation.

**Conversation with Agent**:
```
I have a PDF file with API documentation for "GlobalCargo" carrier.
The PDF contains:
- Authentication details (API key in header)
- Rate calculation endpoint: POST /api/v1/rates
- Shipment creation: POST /api/v1/shipments
- Tracking: GET /api/v1/track/{number}
- Base URL: https://api.globalcargo.com

Please build a complete integration including schemas, mappings, and tests.
```

**Expected Output**:
- ✅ PDF content analysis
- ✅ Structured data extraction
- ✅ Complete integration generation

### **Scenario 4: Mixed Sources Integration**

**Input**: You have multiple sources of information.

**Conversation with Agent**:
```
I need to build an integration for "MultiModal Logistics". I have:

1. A partial OpenAPI spec (rates only)
2. Email correspondence about authentication (OAuth2)
3. A PDF with tracking API details
4. Website documentation for shipment creation

Can you analyze all sources and create a comprehensive integration?

[Provide each source when asked]
```

**Expected Output**:
- ✅ Multi-source analysis
- ✅ Information synthesis
- ✅ Gap identification and recommendations
- ✅ Complete unified integration

## 🔧 Advanced Testing Features

### **Complex Carrier Requirements**

Test the agent with challenging scenarios:

```
Build an integration for "EuroLogistics" with these requirements:
- SOAP API (not REST)
- Complex authentication with certificates
- VAT calculations for EU countries
- Multi-language error messages
- Customs documentation for international shipping
- Special handling for hazardous materials
```

### **Performance Testing**

Test with high-volume scenarios:

```
Create an integration for "HighVolume Express" that needs to:
- Handle 10,000+ rate requests per hour
- Support batch shipment creation
- Implement rate limiting and retry logic
- Cache frequently accessed data
- Generate performance benchmarks
```

### **Legacy System Integration**

Test with older APIs:

```
Build integration for "LegacyFreight" which has:
- XML-only API (no JSON)
- Basic HTTP authentication
- Fixed-width text responses
- No formal documentation (only email examples)
- Proprietary error codes
```

## 📊 Monitoring Agent Performance

### **Success Metrics**

Watch for these indicators during testing:

| Metric | Target | What It Means |
|--------|--------|---------------|
| **Completion Rate** | >95% | Integration completeness |
| **Pattern Recognition** | >25,000 patterns | RAG system effectiveness |
| **Code Quality** | Compilable | Generated code quality |
| **Response Time** | <30 seconds | Agent performance |

### **Real-time Feedback**

The web interface shows:
- 🧠 **Agent thinking process**: Sub-agent coordination
- 🔍 **RAG system queries**: Pattern searches across existing carriers
- ⚙️ **Generation progress**: Schema → Mappings → Tests → Assembly
- 📈 **Quality metrics**: Completion percentages and confidence scores

## 🛠️ Practical Testing Commands

### **Test with Local Files**

```bash
# Test the enhanced tools directly
cd modules/cli/karrio_cli/ai
python test_real_world_scenarios.py
```

### **Simulate Different Input Types**

```python
# In the ADK web interface, you can test:

# 1. OpenAPI spec
"I have this OpenAPI specification: [paste YAML/JSON]"

# 2. Website URL
"Scrape API docs from: https://api.example-carrier.com/docs"

# 3. PDF content
"I extracted this text from a PDF: [paste content]"

# 4. Raw documentation
"Here's the API documentation I have: [paste text]"
```

## 🎯 Expected Results for Production Readiness

### **✅ Complete Integration Package**

Each test should produce:

1. **Python Schemas** - Proper typing, attrs decorators, jstruct serialization
2. **API Mappings** - Request/response transformations for all operations
3. **Test Suites** - Unit tests, integration tests, and fixtures
4. **Configuration Files** - pyproject.toml, settings, provider setup
5. **Documentation** - Usage examples and integration guides

### **✅ Quality Assurance**

Generated code should:
- ✅ Follow Karrio conventions
- ✅ Compile without errors
- ✅ Handle edge cases and errors
- ✅ Include proper logging and debugging
- ✅ Support both sandbox and production modes

## 🚨 Troubleshooting

### **Common Issues and Solutions**

1. **"No patterns found"**
   ```bash
   # Verify RAG system is working
   python test_agent.py
   ```

2. **"Web scraping failed"**
   ```bash
   # Install optional dependencies
   pip install beautifulsoup4 requests
   ```

3. **"PDF parsing not available"**
   ```bash
   # Install PDF dependencies
   pip install PyPDF2 pdfplumber
   ```

4. **"Agent responses are slow"**
   - Check internet connection
   - Verify Google API quota
   - Use a more powerful API tier

## 🎉 Success Criteria

**A successful real-world test should achieve:**

- [ ] **98%+ completion rate** for integration generation
- [ ] **Production-ready code** following Karrio patterns
- [ ] **Multi-format input handling** (OpenAPI, URLs, PDFs, text)
- [ ] **Comprehensive error handling** for all failure scenarios
- [ ] **Complete test coverage** with realistic test data
- [ ] **Performance optimization** for high-volume scenarios

## 🚀 Next Steps After Testing

1. **Code Review**: Examine generated integration code
2. **Sandbox Testing**: Test with actual carrier sandbox APIs
3. **Performance Testing**: Load test the generated integration
4. **Production Deployment**: Deploy to staging environment
5. **Documentation**: Update carrier-specific documentation

---

**💡 Pro Tip**: Start with simple carriers (API key auth, REST APIs) and gradually test more complex scenarios (OAuth, SOAP, legacy systems) to build confidence in the agent's capabilities.

**🔒 Security Note**: Always test with sandbox/development APIs first. Never use production credentials during testing.
