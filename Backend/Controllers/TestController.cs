using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Backend.Models;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TestController : ControllerBase
    {
        private readonly DatabaseContext _context;

        public TestController(DatabaseContext context)
        {
            _context = context;
        }

        // GET: api/Test
        [HttpGet]
        public async Task<ActionResult<IEnumerable<TestDTO>>> GetTest()
        {
          if (_context.Test == null)
          {
              return NotFound();
          }

            var courses = await _context.Test.ToListAsync();
            return courses.Select(c => TestDTO.FromTest(c)).ToList();
        }

        // GET: api/Test/5
        [HttpGet("{id}")]
        public async Task<ActionResult<TestDTO>> GetTest(int id)
        {
          if (_context.Test == null)
          {
              return NotFound();
          }
            var test = await _context.Test.FindAsync(id);

            if (test == null)
            {
                return NotFound();
            }

            return TestDTO.FromTest(test);
        }

        // PUT: api/Test/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutTest(int id, TestDTO test)
        {
            if (id != test.Id)
            {
                return BadRequest();
            }

            var testEntity = await _context.Test.FindAsync(id);
            if (testEntity == null)
            {
                return NotFound();
            }
            testEntity.Questions = test.Questions.Select(q => _context.Question.Find(q)).ToList();
            testEntity.Answers = test.Answers.Select(a => _context.Answer.Find(a)).ToList();
            _context.Entry(testEntity).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!TestExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Test
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<TestDTO>> PostTest(TestDTO test)
        {
          if (_context.Test == null)
          {
              return Problem("Entity set 'DatabaseContext.Test'  is null.");
          }
            var testObj = new Test {
                Id = test.Id,
                Questions = test.Questions.Select(q => _context.Question.Find(q)).ToList(),
                Answers = test.Answers.Select(a => _context.Answer.Find(a)).ToList()
            };
            _context.Test.Add(testObj);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetTest", new { id = test.Id }, test);
        }

        // DELETE: api/Test/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTest(int id)
        {
            if (_context.Test == null)
            {
                return NotFound();
            }
            var test = await _context.Test.FindAsync(id);
            if (test == null)
            {
                return NotFound();
            }

            _context.Test.Remove(test);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool TestExists(int id)
        {
            return (_context.Test?.Any(e => e.Id == id)).GetValueOrDefault();
        }
    }
}
