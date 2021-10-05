mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor = ‘#f5e6c4’\n\
backgroundColor = ‘#F8F9E0’\n\ 
secondaryBackgroundColor = ‘#E4E4E7’\n\
textColor= ‘#3C3C3C’\n\
font = ‘sans serif’\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
