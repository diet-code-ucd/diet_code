// See https://aka.ms/new-console-template for more information
using Microsoft.Extensions.Configuration;
using Azure;
using Azure.AI.OpenAI;

var configuration = new ConfigurationBuilder()
    .AddUserSecrets<Program>()
    .Build();

/*--
might need to add these to test it out
dotnet user-secrets init
dotnet user-secrets set Azure:OpenAI:Endpoint https://oai-test-model.openai.azure.com/
dotnet user-secrets set Azure:OpenAI:ApiKey [contact me]
dotnet user-secrets set Azure:OpenAI:ModelName ITS-test
dotnet add package Microsoft.Extensions.Configuration.UserSecrets
--*/

var openAiClient = new OpenAIClient(
    new Uri(configuration["Azure:OpenAI:Endpoint"]),
    new AzureKeyCredential(configuration["Azure:OpenAI:ApiKey"])
);

var chatCompletionsOptions = new ChatCompletionsOptions
{
    Messages =
    {
        new ChatMessage(ChatRole.System, "You are an assistant"),
        new ChatMessage(ChatRole.User, "Give me 10 math multiple choice questions for a 5th grade student with answers, in json format"),
    }
};

while (true)
{
    Console.WriteLine();
    Console.Write("Bot: ");

    var chatCompletionsResponse = await openAiClient.GetChatCompletionsAsync(
        configuration["Azure:OpenAI:ModelName"],
        chatCompletionsOptions
    );

    var chatMessage = chatCompletionsResponse.Value.Choices[0].Message;
    Console.Write(chatMessage.Content);

    chatCompletionsOptions.Messages.Add(chatMessage);

    Console.WriteLine();

    Console.Write("Enter a message: ");
    var userMessage = Console.ReadLine();
    chatCompletionsOptions.Messages.Add(new ChatMessage(ChatRole.User, userMessage));
}