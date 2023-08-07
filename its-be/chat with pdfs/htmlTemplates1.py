css = '''
<style>
  /* Base style for chat messages */
  .chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
  }

  /* Style for user chat messages */
  .chat-message.user {
    background-color: #2b313e;
    justify-content: flex-end;
  }

  /* Style for bot chat messages */
  .chat-message.bot {
    background-color: #475063;
    justify-content: flex-start;
  }

  /* Style for the avatar */
  .chat-message .avatar {
    width: 20%;
    display: flex;
    align-items: center;
  }

  /* Style for the avatar image */
  .chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
  }

  /* Style for the message text */
  .chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
    word-wrap: break-word; /* To wrap long messages */
  }
'''

bot_template = '''
<!-- Modified HTML code -->
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<!-- Modified HTML code -->
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png" alt="User Avatar">
    </div>    
    <div class="message">{{MSG}}</div>
</div>

'''