import React, { useState } from 'react';
import { Container, TextField, Button, Select, MenuItem, FormControl, InputLabel, Typography, CircularProgress, AppBar, Toolbar, CssBaseline, Box } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Results from './Results';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

const theme = createTheme({
    palette: {
        primary: {
            main: '#1DB954',
        },
        background: {
            default: '#121212'
        },
        text: {
            primary: '#1e1c1c',
        }
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    marginBottom: '20px',
                    borderRadius: '8px',
                    padding: '10px',
                    margin: '10px',
                    backgroundColor: '#1DB954',
                },
            },
        },
        MuiToolbar: {
            styleOverrides: {
                root: {
                    display: 'flex',
                    justifyContent: 'space-between'
                },
            },
        },
        MuiTextField: {
            styleOverrides: {
                root: {
                    margin: '0 10px',
                    backgroundColor: '#fff',
                    borderRadius: '4px',
                },
                input: {
                    color: '#ffffff',
                },
                label: {
                    color: '#000',
                }
            },
        },
        MuiSelect: {
            styleOverrides: {
                root: {
                    color: '#ffffff',
                },
                icon: {
                    color: '#fff',
                },
            },
        },
        MuiMenu: {
            styleOverrides: {
                paper: {
                    backgroundColor: '#282828',
                    color: '#fff',
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    backgroundColor: '#1DB954',
                    color: '#fff',
                    '&:hover': {
                        backgroundColor: '#1ed760',
                    },
                },
            },
        },
    },
});

const App = () => {
    const [query, setQuery] = useState('');
    const [topK, setTopK] = useState(10);
    const [indexingMethod, setIndexingMethod] = useState('Custom Implementation');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [queryTime, setQueryTime] = useState(0);

    const handleSearch = async () => {
        setLoading(true);
        const startTime = performance.now();

        try {
            const response = await fetch('http://127.0.0.1:5000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query,
                    topK,
                    indexingMethod,
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error);
            }

            const data = await response.json();
            const endTime = performance.now();
            setQueryTime(endTime - startTime);

            setResults(data.results);
        } catch (error) {
            console.error('Error during search:', error);
            alert(`Error during search: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Container className="container">
                <AppBar position="static" color="primary">
                    <Toolbar>
                        <TextField
                            label="Enter your query"
                            variant="outlined"
                            size="small"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <TextField
                            label="Top K"
                            type="number"
                            variant="outlined"
                            size="small"
                            value={topK}
                            onChange={(e) => setTopK(e.target.value)}
                        />
                        <FormControl variant="outlined" size="small">
                            <InputLabel style={{ color: '#fff' }}>Indexing Method</InputLabel>
                            <Select
                                value={indexingMethod}
                                onChange={(e) => setIndexingMethod(e.target.value)}
                                label="Indexing Method"
                                MenuProps={{
                                    PaperProps: {
                                        style: {
                                            backgroundColor: '#282828',
                                            color: '#fff',
                                        },
                                    },
                                }}
                            >
                                <MenuItem value="Custom Implementation">Custom Implementation</MenuItem>
                                <MenuItem value="PostgreSQL">PostgreSQL</MenuItem>
                            </Select>
                        </FormControl>
                        <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading}>
                            {loading ? <CircularProgress size={24} /> : 'Search'}
                        </Button>
                    </Toolbar>
                </AppBar>
                {queryTime > 0 && (
                    <Box display="flex" alignItems="center" justifyContent="center" className="query-time">
                        <Typography variant="body1" gutterBottom>
                            Query Time: {queryTime.toFixed(2)} ms
                        </Typography>
                        <AccessTimeIcon style={{ fontSize: 20, color: '#1DB954', marginLeft: '8px' }} />
                    </Box>
                )}
                <div className="results-container">
                    <Results results={results} />
                </div>
            </Container>
        </ThemeProvider>
    );
};

export default App;