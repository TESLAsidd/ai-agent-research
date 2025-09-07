# 🚀 AI Research Agent - Deployment Guide

This guide covers deploying your AI Research Agent for production use and sharing with others.

## 📋 Deployment Options

### 1. Local Development (Current Setup)
- **Best for**: Development, testing, personal use
- **Requirements**: Local Python installation
- **Access**: Only accessible from your machine

### 2. Streamlit Cloud (Recommended for Sharing)
- **Best for**: Sharing with others, public demos
- **Requirements**: GitHub repository, Streamlit Cloud account
- **Access**: Publicly accessible via web URL

### 3. Docker Deployment
- **Best for**: Production environments, consistent deployment
- **Requirements**: Docker installed
- **Access**: Accessible via container

### 4. Cloud Platforms (AWS, GCP, Azure)
- **Best for**: Enterprise use, high availability
- **Requirements**: Cloud platform account
- **Access**: Scalable cloud deployment

## 🌐 Option 1: Streamlit Cloud Deployment

### Step 1: Prepare Repository
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial AI Research Agent deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/ai-research-agent.git
git push -u origin main
```

### Step 2: Configure Streamlit Cloud
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Add secrets for API keys

### Step 3: Configure Secrets
In Streamlit Cloud dashboard, add these secrets:

```toml
[secrets]
OPENAI_API_KEY = "your-openai-api-key"
GOOGLE_SEARCH_API_KEY = "your-google-api-key"
GOOGLE_SEARCH_ENGINE_ID = "your-search-engine-id"
SERPAPI_API_KEY = "your-serpapi-key"
BING_SEARCH_API_KEY = "your-bing-api-key"
NEWSAPI_KEY = "your-newsapi-key"
```

### Step 4: Deploy
1. Click "Deploy!"
2. Wait for deployment to complete
3. Access your app via the provided URL

## 🐳 Option 2: Docker Deployment

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  ai-research-agent:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_SEARCH_API_KEY=${GOOGLE_SEARCH_API_KEY}
      - GOOGLE_SEARCH_ENGINE_ID=${GOOGLE_SEARCH_ENGINE_ID}
      - SERPAPI_API_KEY=${SERPAPI_API_KEY}
      - BING_SEARCH_API_KEY=${BING_SEARCH_API_KEY}
      - NEWSAPI_KEY=${NEWSAPI_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Step 3: Build and Run
```bash
# Build Docker image
docker build -t ai-research-agent .

# Run with docker-compose
docker-compose up -d

# Or run directly
docker run -p 8501:8501 --env-file .env ai-research-agent
```

## ☁️ Option 3: Cloud Platform Deployment

### AWS EC2 Deployment
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Clone repository
git clone https://github.com/yourusername/ai-research-agent.git
cd ai-research-agent

# Set environment variables
export OPENAI_API_KEY="your-key"
export GOOGLE_SEARCH_API_KEY="your-key"
# ... other keys

# Run with Docker
docker-compose up -d
```

### Google Cloud Platform
```bash
# Create Cloud Run service
gcloud run deploy ai-research-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key
```

### Azure Container Instances
```bash
# Create container group
az container create \
  --resource-group myResourceGroup \
  --name ai-research-agent \
  --image ai-research-agent \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=your-key
```

## 🔧 Production Configuration

### Environment Variables
Create a production `.env` file:

```env
# Production settings
OPENAI_API_KEY=your-production-key
GOOGLE_SEARCH_API_KEY=your-production-key
GOOGLE_SEARCH_ENGINE_ID=your-production-id
SERPAPI_API_KEY=your-production-key
BING_SEARCH_API_KEY=your-production-key
NEWSAPI_KEY=your-production-key

# Performance settings
MAX_SEARCH_RESULTS=15
MAX_CONTENT_LENGTH=8000
SEARCH_TIMEOUT=45
MAX_TOKENS=3000
```

### Security Considerations
1. **API Key Protection**: Never commit API keys to version control
2. **Rate Limiting**: Implement rate limiting for production use
3. **Input Validation**: Validate all user inputs
4. **Error Handling**: Implement comprehensive error handling
5. **Logging**: Set up proper logging for monitoring

### Performance Optimization
1. **Caching**: Implement caching for repeated queries
2. **Database**: Add database for storing research history
3. **Load Balancing**: Use load balancers for high traffic
4. **CDN**: Use CDN for static assets

## 📊 Monitoring and Maintenance

### Health Checks
```python
# Add to app.py
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Backup Strategy
1. **Code Backup**: Regular git commits and pushes
2. **Data Backup**: Backup research history and user data
3. **Configuration Backup**: Secure backup of environment variables

## 🚀 Quick Start Commands

### Local Development
```bash
# Activate virtual environment
source ai_research_env/bin/activate  # Linux/Mac
ai_research_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Docker Deployment
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Streamlit Cloud
```bash
# Push to GitHub
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main

# Deploy via Streamlit Cloud dashboard
```

## 🔍 Troubleshooting Deployment

### Common Issues

#### Issue 1: API Key Not Working
- Check environment variables are set correctly
- Verify API keys are valid and active
- Check API usage limits

#### Issue 2: Port Conflicts
```bash
# Use different port
streamlit run app.py --server.port 8502
```

#### Issue 3: Memory Issues
- Reduce `MAX_SEARCH_RESULTS` in config
- Implement pagination
- Use smaller AI models

#### Issue 4: Network Timeouts
- Increase `SEARCH_TIMEOUT` in config
- Implement retry logic
- Use connection pooling

### Debug Mode
```bash
# Run with debug information
streamlit run app.py --logger.level debug
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use multiple instances behind load balancer
- Implement session affinity
- Use shared database for state

### Vertical Scaling
- Increase memory and CPU
- Optimize AI model usage
- Implement caching layers

### Cost Optimization
- Use free tiers where possible
- Implement usage quotas
- Monitor API costs

## 🎯 Success Metrics

### Performance Metrics
- Response time < 30 seconds
- Uptime > 99%
- Error rate < 1%

### User Metrics
- Research queries per day
- User satisfaction scores
- Feature usage statistics

---

**🎉 Congratulations!** Your AI Research Agent is now ready for production deployment!
