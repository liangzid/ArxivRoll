import shutil
import os

def copy_folder(source_folder, destination_folder):
    try:
        if not os.path.exists(source_folder):
            print(f"files '{source_folder}' not exist.")
            return
        
    
        destination_path = os.path.join(destination_folder, os.path.basename(source_folder))
        
        if os.path.exists(destination_path):
            print(f"files '{destination_path}' exist, remove it first.")
            shutil.rmtree(destination_path)  
        
        shutil.copytree(source_folder, destination_path)
        print(f"files '{source_folder}' have copied to '{destination_path}'。")
        
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    #"EleutherAI/gpt-j-6b", "01-ai/Yi-1.5-34B-Chat","meta-llama/Llama-4-Scout-17B-16E-Instruct" "openai/gpt-3.5-turbo", "openai/gpt-5"
    models=[ "openai/gpt-4o",
	"openai/gpt-4",
    "anthropic/claude-3.5-sonnet",
	"anthropic/claude-3.7-sonnet",
	"anthropic/claude-sonnet-4",
	"anthropic/claude-opus-4",
	"google/gemini-2.0-flash-001",
	"google/gemini-2.5-flash",
	"google/gemini-2.5-pro",
	"deepseek/deepseek-chat-v3.1",
	"deepseek/deepseek-chat-v3-0324" ,
	"deepseek/deepseek-r1-0528",
	"moonshotai/kimi-k2" 
	]
    task='arxivrollbench2025a-50'
    for model in models:
        # source = f'/home/zi/arxivSpider/eval/RES_OPENSOURCE/{model}{task}'
        #opensuorce
        source = f'/home/zi/arxivSpider/eval/0721_newcloseAIs/{model}{task}'
        destination = f'/home/zi/arxivSpider/robench2025a_results'
        copy_folder(source, destination)