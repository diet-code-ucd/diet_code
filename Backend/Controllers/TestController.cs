using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Backend.Models;
using Backend.Codecs;
using Backend.Services;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TestController : ControllerBase
    {
        private readonly DatabaseContext _context;
        private readonly ITestService _testService;

        public TestController(DatabaseContext context, ITestService testService)
        {
            _context = context;
            _testService = testService;
        }

        // GET: api/Test
        [HttpGet]
        public async Task<ActionResult<IEnumerable<TestDTO>>> GetTest()
        {
            if (_context.Tests == null)
            {
                return NotFound();
            }

            var courses = await _context.Tests.ToListAsync();
            return courses.Select(c => TestDTO.FromTest(c)).ToList();
        }

        // GET: api/Test/5
        [HttpGet("{id}")]
        public async Task<ActionResult<TestDTO>> GetTest(int id)
        {
            if (_context.Tests == null)
            {
                return NotFound();
            }
            var test = await _context.Tests.FindAsync(id);

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
            if (id != test.TestId)
            {
                return BadRequest();
            }

            var testEntity = await _context.Tests.FindAsync(id);
            if (testEntity == null)
            {
                return NotFound();
            }
            //TODO: fix these for nulls
            testEntity.Questions = test.Questions.Select(q => _context.Questions.Find(q)).ToList();
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

        [HttpPost("generate")]
        public async Task<ActionResult<TestDTO>> PostGenerateTest(GenerateTest generateTest)
        {
            var course = await _context.Courses.FindAsync(generateTest.CourseId);
            var user = await _context.Users.FindAsync(generateTest.UserId);
            if (course == null || user == null)
            {
                return NotFound();
            }
            
            Test test = await _testService.GenerateTest(course, user, generateTest.Difficulty, generateTest.NumberOfQuestions);
            _context.Tests.Add(test);
            
            user.Tests.Add(test);

            _context.Entry(user).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                throw;
            }

            return TestDTO.FromTest(test);
        }

        [HttpPost("submit")]
        public async Task<ActionResult<TestResult>> PostSubmitTest(TestSubmission test)
        {
            TestResult testResult = _testService.GradeTest(test);

            return testResult;
        }

        // POST: api/Test
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<TestDTO>> PostTest(TestDTO test)
        {
            if (_context.Tests == null)
            {
                return Problem("Entity set 'DatabaseContext.Test'  is null.");
            }
            var testObj = new Test
            {
                Id = test.TestId,
                //TODO: fix these for nulls
                Questions = test.Questions.Select(q => _context.Questions.Find(q.QuestionId)).ToList()
            };
            _context.Tests.Add(testObj);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetTest", new { id = test.TestId }, test);
        }

        // DELETE: api/Test/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTest(int id)
        {
            if (_context.Tests == null)
            {
                return NotFound();
            }
            var test = await _context.Tests.FindAsync(id);
            if (test == null)
            {
                return NotFound();
            }

            _context.Tests.Remove(test);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool TestExists(int id)
        {
            return (_context.Tests?.Any(e => e.Id == id)).GetValueOrDefault();
        }
    }
}
