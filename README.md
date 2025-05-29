# Bulk IPO Manager v2.0

A modern, robust bulk IPO application system for MeroShare built with clean architecture and best practices.

## 🚀 Features

- **Bulk IPO Applications**: Apply for IPOs across multiple accounts simultaneously
- **Concurrent Processing**: Configurable concurrent request handling with rate limiting
- **Robust Error Handling**: Comprehensive error handling with retry mechanisms
- **Clean Architecture**: SOLID principles, DRY code, and separation of concerns
- **Configurable Settings**: Environment variable support and flexible configuration
- **Detailed Logging**: Comprehensive logging with rotation and different levels
- **Progress Tracking**: Real-time progress indicators and detailed results
- **Retry Mechanism**: Automatic retry for failed applications
- **Results Analytics**: Detailed statistics and error analysis

## 📁 Project Structure

```
bulk-ipo/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Application settings and configuration
│   │   └── constants.py         # Application constants
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model with validation
│   │   ├── ipo_application.py   # IPO application tracking
│   │   └── application_result.py # Results with analytics
│   ├── services/
│   │   ├── __init__.py
│   │   ├── account_service.py   # Account management
│   │   ├── ipo_service.py       # IPO operations
│   │   └── application_service.py # Bulk application processing
│   ├── api/
│   │   ├── __init__.py
│   │   └── meroshare_client.py  # MeroShare API client
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py        # Custom exceptions
│       └── logger.py           # Logging utilities
├── main.py                     # Main application entry point
├── accounts.txt               # User accounts file
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd bulk-ipo
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup accounts file**:
   Create `accounts.txt` with your MeroShare account details:
   ```
   # Format: client_id,username,password,crn,pin
   12345,your_username,your_password,your_crn,1234
   67890,another_username,another_password,another_crn,5678
   ```

## 🚀 Usage

### Basic Usage

Run the application:

```bash
python main.py
```

### Environment Variables

Configure the application using environment variables:

```bash
# Concurrency settings
export IPO_MAX_CONCURRENT=3
export IPO_RATE_LIMIT_DELAY=2.0

# Retry settings
export IPO_MAX_RETRIES=5

# Logging
export IPO_DETAILED_LOGGING=true
```

### Configuration Options

The application supports various configuration options in `src/config/settings.py`:

- **Concurrency**: `MAX_CONCURRENT_REQUESTS`, `RATE_LIMIT_DELAY`
- **Retry Logic**: `MAX_RETRY_ATTEMPTS`, `AUTO_RETRY_FAILED`
- **Logging**: `DETAILED_LOGGING`, `SAVE_DETAILED_LOGS`
- **File Paths**: `ACCOUNTS_FILE`, `RESULTS_FILE`, `LOG_DIR`

## 📊 Features in Detail

### 1. Account Management

- CSV-based account loading with validation
- Support for comments and empty lines in accounts file
- Comprehensive account validation

### 2. IPO Processing

- Fetch available IPOs automatically
- Interactive IPO selection with validation
- Kitta amount validation against IPO limits

### 3. Bulk Application

- Concurrent processing with configurable limits
- Rate limiting to prevent API overload
- Real-time progress tracking
- Comprehensive error handling

### 4. Results & Analytics

- Detailed success/failure statistics
- Error categorization and analysis
- Results saved to JSON file
- Duration tracking and performance metrics

### 5. Retry Mechanism

- Automatic retry for failed applications
- Configurable retry attempts and delays
- Exponential backoff support

## 🔧 Architecture

### SOLID Principles

- **Single Responsibility**: Each class has a single, well-defined purpose
- **Open/Closed**: Easy to extend without modifying existing code
- **Liskov Substitution**: Proper inheritance and interface design
- **Interface Segregation**: Focused, minimal interfaces
- **Dependency Inversion**: Depends on abstractions, not concretions

### Design Patterns

- **Service Layer Pattern**: Business logic separated into services
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Object creation abstraction
- **Singleton Pattern**: Configuration management

### Error Handling

- Custom exception hierarchy
- Graceful degradation
- Comprehensive logging
- User-friendly error messages

## 📝 Logging

The application provides comprehensive logging:

- **Console Output**: Real-time progress and status
- **File Logging**: Detailed logs with rotation
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: Automatic cleanup of old log files

Logs are stored in the `logs/` directory with automatic rotation.

## 🔒 Security

- Passwords are not logged or stored in results
- Secure handling of authentication tokens
- Input validation and sanitization
- Rate limiting to prevent abuse

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Failures**:

   - Verify account credentials in `accounts.txt`
   - Check if accounts are active and not locked

2. **Network Errors**:

   - Check internet connection
   - Verify MeroShare API availability
   - Adjust timeout settings if needed

3. **Rate Limiting**:

   - Increase `RATE_LIMIT_DELAY` if getting rate limited
   - Reduce `MAX_CONCURRENT_REQUESTS`

4. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python path configuration

### Debug Mode

Enable detailed logging for debugging:

```bash
export IPO_DETAILED_LOGGING=true
python main.py
```

## 📈 Performance

- **Concurrent Processing**: Up to 10 concurrent requests (configurable)
- **Rate Limiting**: Configurable delays between requests
- **Memory Efficient**: Streaming processing for large account lists
- **Optimized API Calls**: Minimal API requests per application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing architecture
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with MeroShare's terms of service and applicable regulations. The developers are not responsible for any misuse or consequences arising from the use of this software.

## 🔄 Version History

### v2.0.0 (Current)

- Complete architecture refactoring
- SOLID principles implementation
- Improved error handling and logging
- Concurrent processing with rate limiting
- Comprehensive configuration management
- Enhanced user experience

### v1.0.0 (Legacy)

- Basic bulk IPO application functionality
- Monolithic architecture
- Limited error handling

---

**Built with ❤️ for the MeroShare community**
