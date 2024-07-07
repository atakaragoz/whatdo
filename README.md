# whatdo
python application for me to track productivity. Interfaces with obsidian because it's all markdown files. Idea is to store a set of todo items and then surface them by automatically placing them at the start of my daily journal. 

## Roadmap
- [x] create config file that takes in obsidian vault path, daily journal length, and a todo file path
- [x] think about a format for todo items and what might be necessary. Item, due date, priority, tags, etc.
- [x] simple command line interface to add individual items to the todo list OR can add to the todo list by looking up the file in obsidian and adding the item to the end of the file
- [ ] function that gets called at the start of the day that takes items from the todo list and adds it to the start of the daily journal
    - [ ] if the items have been crossed off in the daily journal then they are removed from the todo list, added to a completed list
    - [ ] if the items have not been crossed off in the daily journal then they are copied over to the following day

## Notes
- Should be easy by looking for - [ ] or - [x] in daily journal markdown file.
Format in the actual broader todo list should be almost like a table:
```markdown
| Item | Due Date | Priority | Estimated Time | Tags |
| ---- | -------- | -------- | --------| ---- |
| Item 1 | 2024-08-08 | 1 | 2 hours | tag1, tag2 |

```
- Other custom things can be added later like if the todo item is related to reading a paper I can also add a summary or my notes on the paper in a file to link in the completed list.
- likewise the ability to store notes along with the completed item might be useful? I wonder if there's a programmatic way to generate custom ids to link back to the item.
