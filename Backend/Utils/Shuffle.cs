// From https://stackoverflow.com/questions/273313/randomize-a-listt
namespace Backend.Utils
{
    public static class Shuffle
    {
        public static void ShuffleList<T>(this IList<T> list)
        {
            var rng = new Random();
            var n = list.Count;
            while (n > 1) {
                n--;
                var k = rng.Next(n + 1);
                var value = list[k];
                list[k] = list[n];
                list[n] = value;
            }
        }
    }
}