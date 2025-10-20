# Hospital LLM - Frontend

React-based web application providing an intuitive interface for RAG testing, evaluation, data visualization, and interactive document Q&A.

## Overview

The frontend is a single-page application (SPA) built with React and Vite, offering:

- **Interactive Dashboard**: Visualize test results with charts and statistics
- **Test Management**: Configure and run tests through a web UI
- **Q&A Editor**: Create and manage question-answer pairs
- **Chat Interface**: Real-time document Q&A with configurable settings
- **Results Explorer**: Filter and analyze test execution results
- **Vector DB Manager**: Create and manage vector databases
- **System Prompts**: Template management for LLM system messages

## Getting Started

### Prerequisites

- Node.js 16 or higher (tested with Node v22.13.1)
- npm 7+ (tested with npm 10.9.2)
- Backend server running at `http://127.0.0.1:8000`

### Installation

```bash
npm install
```

### Running the Application

**Development server with hot reload:**
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

**Build for production:**
```bash
npm run build
```

**Lint code:**
```bash
npm run lint
```

**Auto-fix linting issues:**
```bash
npm run lint:fix
```

## Features

### 1. Dashboard (Data Visualization)

- Visualize test results with interactive bar charts
- Group data by run count, LLM model, embedding model, chunk size, etc.
- View average evaluation scores and chunk scores
- Detailed tooltips with run attributes

**Important:** Dashboard automatically filters out tests without `run_count` field.

### 2. Results Explorer

- Browse all test execution results
- Filter by LLM model, embedding model, run count, scores
- View responses, retrieved chunks, evaluations
- Export filtered results

### 3. Interactive Chat

- Real-time document Q&A
- Configure LLM model and retrieval settings
- View AI responses and retrieved chunks

### 4. Test Configurator

- Create and manage test cases
- Configure LLM, embeddings, chunking parameters
- Run tests directly from UI

### 5. Q&A Editor

- Create question-answer pairs
- Organize into batches
- Associate with test cases

### 6. Vector Database Manager

- List and manage vector databases
- Create new databases with custom embeddings
- Load specific databases

### 7. System Prompts

- Create and manage system prompt templates
- Use templates in test configurations

## Architecture

### Project Structure

```
src/
├── App.jsx              # Main application component
├── components/          # Shared UI components
├── features/            # Feature modules (dashboard, chat, testing, etc.)
├── store/               # Redux store and slices
├── hooks/               # Custom React hooks
├── utils/               # Utility functions
├── constants/           # Application constants
└── styles/              # Global styles
```

### Redux Store

The application uses Redux Toolkit for state management with the following slices:

- **results**: Test execution results
- **runs**: Run attributes indexed by run_count
- **tests**: Test configurations
- **qa** / **qaBatches**: Q&A data
- **systemPrompts**: System prompts
- **vectorDBs**: Vector database management
- **config**: Application configuration
- **filters**: Filter state
- **chat**: Chat interface state
- **toast**: Notifications

### Custom Hooks

```javascript
import { useAppDispatch } from './hooks/useAppDispatch';
import { useAppSelector } from './hooks/useAppSelector';

const dispatch = useAppDispatch();
const results = useAppSelector(state => state.results.filteredData);
```

## API Configuration

API endpoint is configured in `src/constants/index.js`:

```javascript
export const API_BASE_URL = 'http://127.0.0.1:8000';
```

## Styling

The application uses Tailwind CSS for styling. Global styles are in `src/styles/tailwind.css`.

## Working with the Dashboard

The dashboard filters test data to only show tests with `run_count`:

```javascript
const filteredData = rawData.filter(
  item => item.run_count !== undefined && item.run_count !== null
);
```

## Development

### Adding a New Feature

1. Create feature directory in `src/features/`
2. Create Redux slice in `src/store/slices/`
3. Add reducer to `src/store/index.js`
4. Add route/tab in `src/constants/index.js`
5. Integrate in `src/App.jsx`

## Troubleshooting

### Build Errors
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

### Runtime Errors
- Verify backend is running at correct URL
- Check Redux state in Redux DevTools
- Verify API endpoint configuration

### Empty Dashboard
- Ensure test data has `run_count` field
- Check backend connectivity
- Verify data is being fetched

## Dependencies

### Core
- **react** (^18.2.0)
- **@reduxjs/toolkit** (^2.8.2)
- **react-redux** (^9.2.0)
- **recharts** (^2.15.2)
- **react-select** (^5.10.2)
- **tailwindcss** (^4.1.12)

### Development
- **vite** (^7.1.3)
- **eslint**

## Related Documentation

- [../README.md](../README.md) - Overall project documentation
- [../backend/README.md](../backend/README.md) - Backend documentation
- [../CLAUDE.md](../CLAUDE.md) - Architecture guidance
