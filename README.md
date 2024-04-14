# About
a POC text based room escape to test LLM (Large Language Model eg. Llama2 ChatGPT).
A LLM agent is put inside the room and play the game, by function calling

# Install
## install the "game"
```
git clone git@github.com:ylchan87/LLMRoomEscape.git
cd LLMRoomEscape
python3 -m pip install -e .
```

## install ChatGLM3 for use as AI player
```
cd LLMRoomEscape
git submodule update --init --resursive
cd ext_deps/ChatGLM3
python3 -m pip install -r requirements.txt
```

# Test
python -m unittest discover -v