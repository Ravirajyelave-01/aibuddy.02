"""
Basic functionality tests for Voice Assistant
"""
from models import Command, CommandIntent, Message, MessageType
from command_processor import CommandProcessor
from datetime import datetime

def test_models():
    """Test data models"""
    print("Testing data models...")
    
    # Test Command
    cmd = Command(
        intent=CommandIntent.OPEN_APP,
        parameters={'app_name': 'chrome'},
        raw_text='open chrome'
    )
    assert cmd.intent == CommandIntent.OPEN_APP
    assert cmd.parameters['app_name'] == 'chrome'
    
    # Test Message
    msg = Message(
        type=MessageType.USER,
        content='Hello',
        timestamp=datetime.now()
    )
    assert msg.type == MessageType.USER
    assert msg.content == 'Hello'
    
    print("✓ Data models working correctly")

def test_command_processor():
    """Test command processing"""
    print("\nTesting command processor...")
    
    processor = CommandProcessor()
    
    # Test open app command
    cmd = processor.process_command("open chrome")
    assert cmd.intent == CommandIntent.OPEN_APP
    assert cmd.parameters['app_name'] == 'chrome'
    print("✓ Open app command recognized")
    
    # Test music command
    cmd = processor.process_command("play despacito")
    assert cmd.intent == CommandIntent.PLAY_MUSIC
    assert cmd.parameters['song_name'] == 'despacito'
    print("✓ Music command recognized")
    
    # Test exit command
    cmd = processor.process_command("bye")
    assert cmd.intent == CommandIntent.EXIT
    print("✓ Exit command recognized")
    
    # Test question
    cmd = processor.process_command("what is the weather")
    assert cmd.intent == CommandIntent.ANSWER_QUESTION
    print("✓ Question command recognized")
    
    print("✓ Command processor working correctly")

if __name__ == "__main__":
    try:
        test_models()
        test_command_processor()
        print("\n✅ All basic tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
