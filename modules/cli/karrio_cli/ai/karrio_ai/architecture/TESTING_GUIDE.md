# Testing Karrio ADK Agent with Real-World Carriers

This guide shows you how to test the Karrio ADK (Application Development Kit) agent with real shipping carriers using the web interface.

## Prerequisites

### 1. Environment Setup

First, make sure you have the development environment activated:

```bash
# From the karrio root directory
source ./bin/activate-env
```

### 2. Google API Key

You need a Google API key to use the Gemini AI model:

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new API key or use an existing one
3. Enable the "Generative Language API" for your project

### 3. Environment Configuration

1. Copy the environment sample file:
```bash
cd modules/cli/karrio_cli/ai
cp .env.sample .env
```

2. Edit the `.env` file and replace `YOUR_GOOGLE_API_KEY_HERE` with your actual API key:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

## Starting the ADK Web Interface

### Method 1: Using CLI Command (Recommended)

```bash
# From the karrio root directory
python -m karrio_cli agent web
```

### Method 2: Direct ADK Command

```bash
# From the karrio root directory
cd modules/cli/karrio_cli/ai
adk web karrio_ai
```

The web interface will start on `http://localhost:8080` (or the port specified in your .env file).

## Testing with Real Carriers

### Scenario 1: Building a New Carrier Integration

Let's test building an integration for a hypothetical carrier called "SwiftShip":

1. **Open the web interface** at `http://localhost:8080`

2. **Start a conversation** with the agent:
   ```
   I want to build a new carrier integration for SwiftShip. They have a REST API with:
   - Rates endpoint: https://api.swiftship.com/v1/rates
   - Shipments endpoint: https://api.swiftship.com/v1/shipments
   - Tracking endpoint: https://api.swiftship.com/v1/tracking
   - Authentication: API key in header
   ```

3. **Ask for analysis** of similar carriers:
   ```
   What existing carriers are most similar to SwiftShip?
   Can you analyze UPS, FedEx, and DHL Express to find patterns?
   ```

4. **Request schema generation**:
   ```
   Generate Python schemas for SwiftShip based on this API documentation:
   {
     "rate_response": {
       "rates": [
         {
           "service_code": "GROUND",
           "service_name": "Ground Service",
           "total_cost": 15.99,
           "currency": "USD",
           "delivery_days": 3
         }
       ]
     }
   }
   ```

5. **Ask for complete integration**:
   ```
   Generate a complete SwiftShip integration with all components:
   - Schemas
   - Mappings
   - Tests
   - Configuration files
   ```

### Scenario 2: Analyzing Existing Carriers

Test the agent's analysis capabilities:

1. **Analyze a complex carrier**:
   ```
   Analyze the FedEx connector and show me:
   - Authentication patterns
   - Rate mapping examples
   - Error handling approaches
   - Test structure
   ```

2. **Compare multiple carriers**:
   ```
   Compare the authentication methods used by UPS, FedEx, and DHL Express.
   What are the common patterns and best practices?
   ```

3. **Extract specific patterns**:
   ```
   Extract the rate calculation patterns from all North American carriers.
   Show me code examples of how they handle package dimensions.
   ```

### Scenario 3: Testing Edge Cases

Test the agent's robustness:

1. **Complex API structures**:
   ```
   How would you handle a carrier with XML-only APIs and SOAP authentication?
   Show me an example integration approach.
   ```

2. **International requirements**:
   ```
   Build an integration for a European carrier that requires:
   - Customs documentation
   - VAT calculations
   - Multi-language support
   ```

3. **Performance optimization**:
   ```
   How would you optimize the rate calculation for a carrier that
   requires separate API calls for each service type?
   ```

## Expected Agent Capabilities

When testing, the agent should demonstrate:

### ✅ Analysis Capabilities
- [ ] Analyze 100+ existing carrier files
- [ ] Extract 25,000+ code patterns
- [ ] Identify similar carriers based on API characteristics
- [ ] Generate best practice recommendations

### ✅ Generation Capabilities
- [ ] Generate complete Python schemas with proper typing
- [ ] Create request/response mappings for all operations
- [ ] Build comprehensive test suites
- [ ] Assemble complete project structure

### ✅ Integration Features
- [ ] Multi-agent coordination (Schema, Mapping, Integration, Testing agents)
- [ ] RAG system with semantic search
- [ ] Pattern-based code generation
- [ ] Quality assurance and validation

## Monitoring Agent Performance

### Real-time Feedback

The web interface should show:
- **Agent thinking process**: Sub-agent coordination
- **RAG system queries**: Pattern searches and code examples
- **Generation progress**: Schema → Mappings → Tests → Assembly
- **Quality metrics**: Completion percentage and confidence scores

### Performance Metrics

Monitor these key indicators:
- **Response time**: < 30 seconds for complex integrations
- **Accuracy**: Generated code should compile and follow Karrio conventions
- **Completeness**: Should achieve 95%+ completion rate
- **Pattern quality**: High-confidence (>0.7) pattern matches

## Troubleshooting

### Common Issues

1. **"ADK command not found"**
   ```bash
   pip install google-cloud-aiplatform[dev]
   ```

2. **"Google API key not set"**
   - Check your `.env` file
   - Verify the API key is correct
   - Ensure Generative Language API is enabled

3. **"RAG system shows 0 patterns"**
   - Verify workspace path is correct
   - Check that connector files exist
   - Run the basic test: `python test_agent.py`

4. **"Agent responses are slow"**
   - Check internet connection
   - Verify API quota hasn't been exceeded
   - Consider using a more powerful model tier

### Debug Mode

Enable debug logging by setting in your `.env`:
```bash
DEBUG=TRUE
LOG_LEVEL=DEBUG
```

## Advanced Testing Scenarios

### Custom Scenario Templates

1. **High-Volume Carrier**:
   ```
   Test integration for a carrier handling 10,000+ shipments/day
   with rate limiting and batch processing requirements.
   ```

2. **Multi-Modal Carrier**:
   ```
   Build integration for carrier supporting air, ground, and ocean freight
   with different API endpoints and authentication for each mode.
   ```

3. **White-Label Integration**:
   ```
   Create a flexible integration that can be configured for multiple
   white-label carriers sharing the same API platform.
   ```

## Success Criteria

A successful test should result in:

- [ ] **98%+ completion rate** for integration generation
- [ ] **Production-ready code** that follows Karrio conventions
- [ ] **Comprehensive test coverage** with unit and integration tests
- [ ] **Proper error handling** for all failure scenarios
- [ ] **Complete documentation** with usage examples

## Next Steps

After successful testing:

1. **Code Review**: Review generated integration code
2. **Real API Testing**: Test with actual carrier sandbox APIs
3. **Performance Testing**: Load test the generated integration
4. **Production Deployment**: Deploy to staging environment
5. **Documentation**: Update carrier-specific documentation

---

**Note**: Remember that this is an AI-powered tool. Always review generated code before production use and test thoroughly with real carrier APIs in sandbox mode first.
