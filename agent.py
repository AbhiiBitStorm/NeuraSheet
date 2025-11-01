from llama_cpp import Llama
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from typing import Optional, List, Any
import config
from tools import ExcelTools

# Custom LLM wrapper for Mistral
class MistralLLM(LLM):
    """Mistral 7B ko LangChain ke saath use karne ke liye wrapper"""
    
    llm: Any = None
    
    def __init__(self):
        super().__init__()
        print("🔄 Loading Mistral 7B model...")
        self.llm = Llama(**config.LLM_CONFIG)
        print("✅ Mistral 7B loaded successfully!")
    
    @property
    def _llm_type(self) -> str:
        return "mistral-7b"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """LLM ko call karo"""
        response = self.llm(
            prompt,
            max_tokens=config.LLM_CONFIG["max_tokens"],
            temperature=config.LLM_CONFIG["temperature"],
            top_p=config.LLM_CONFIG["top_p"],
            stop=stop or []
        )
        return response["choices"][0]["text"].strip()


# Excel Agent class
class ExcelAgent:
    """Main Excel Agent"""
    
    def __init__(self):
        print("🚀 Initializing Excel Agent...")
        
        # LLM load karo
        self.llm = MistralLLM()
        
        # Excel tools instance
        self.excel_tools = ExcelTools()
        
        # Tools define karo
        self.tools = self._create_tools()
        
        # Agent banao
        self.agent = self._create_agent()
        
        print("✅ Excel Agent ready!")
    
    def _create_tools(self):
        """LangChain tools banao"""
        
        tools = [
            Tool(
                name="read_excel",
                func=lambda x: self.excel_tools.read_excel(x),
                description="Excel file read karne ke liye. Input: file path string"
            ),
            Tool(
                name="get_data_info",
                func=lambda x: self.excel_tools.get_data_info(),
                description="Excel data ki information lene ke liye (rows, columns, etc.)"
            ),
            Tool(
                name="calculate_sum",
                func=lambda x: self.excel_tools.calculate_sum(x),
                description="Kisi column ka sum calculate karne ke liye. Input: column name"
            ),
            Tool(
                name="calculate_average",
                func=lambda x: self.excel_tools.calculate_average(x),
                description="Kisi column ka average calculate karne ke liye. Input: column name"
            ),
            Tool(
                name="filter_data",
                func=lambda x: self._filter_helper(x),
                description="Data filter karne ke liye. Input format: 'column_name,value'"
            ),
            Tool(
                name="sort_data",
                func=lambda x: self.excel_tools.sort_data(x),
                description="Data sort karne ke liye. Input: column name"
            ),
            Tool(
                name="save_excel",
                func=lambda x: self.excel_tools.save_excel(x),
                description="Modified Excel file save karne ke liye. Input: output file path"
            ),
        ]
        
        return tools
    
    def _filter_helper(self, input_str):
        """Filter tool ke liye helper"""
        try:
            parts = input_str.split(',')
            column = parts[0].strip()
            value = parts[1].strip()
            return self.excel_tools.filter_data(column, value)
        except:
            return "❌ Format error! Use: 'column_name,value'"
    
    def _create_agent(self):
        """ReAct agent banao"""
        
        # Custom prompt template
        template = """You are an Excel expert AI agent. Help users with Excel tasks.

You have access to these tools:
{tools}

Tool Names: {tool_names}

Use this format:
Question: the input question
Thought: think about what to do
Action: the action to take (must be one of [{tool_names}])
Action Input: input for the action
Observation: result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
        )
        
        # Agent create karo
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Executor banao
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
        
        return agent_executor
    
    def run(self, task):
        """Agent ko task do"""
        print(f"\n🎯 Task: {task}\n")
        try:
            result = self.agent.invoke({"input": task})
            return result
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def chat(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("💬 Excel Agent Chat Mode")
        print("="*60)
        print("Commands:")
        print("  - Type your Excel task")
        print("  - Type 'quit' to exit")
        print("="*60 + "\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            result = self.run(user_input)
            print(f"\n🤖 Agent: {result.get('output', result)}\n")


# Main execution
if __name__ == "__main__":
    # Agent initialize karo
    agent = ExcelAgent()
    
    # Chat mode start karo
    agent.chat()