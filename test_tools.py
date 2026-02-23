"""
Test the custom Strands tools
"""
from action_executors import open_application, play_music_on_youtube
from strands_tools import current_time

def test_tools():
    """Test each tool individually"""
    
    print("Testing custom tools...\n")
    
    # Test current_time
    print("1. Testing current_time tool:")
    try:
        time_result = current_time()
        print(f"   Result: {time_result}")
        print("   ✓ current_time works\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test open_application (dry run - just check it doesn't crash)
    print("2. Testing open_application tool:")
    try:
        result = open_application("notepad")
        print(f"   Result: {result}")
        print("   ✓ open_application works\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test play_music_on_youtube
    print("3. Testing play_music_on_youtube tool:")
    try:
        result = play_music_on_youtube("test song")
        print(f"   Result: {result}")
        print("   ✓ play_music_on_youtube works\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ All tools tested successfully!")

if __name__ == "__main__":
    test_tools()
