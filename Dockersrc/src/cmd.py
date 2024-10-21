import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import TaskModel
from sqlalchemy import select, delete

engine = create_engine("sqlite:///./site.db")
new_session = sessionmaker(engine, expire_on_commit=False)


@click.group()
def hello():
    return


@hello.command()
def get_all_tasks():
    """
    Get all tasks.
    """
    with new_session() as session:
        query = select(TaskModel)
        result = session.execute(query)
        tasks = result.scalars().all()
        if len(tasks) == 0:
            click.echo('tasks is empty.')
            return
        for task in tasks:
            click.echo(f'id={task.id}    description={task.description}    complete={task.complete}\n')


@hello.command()
@click.argument('task_id')
def get_task(task_id):
    """
    Get task by <TASK_ID>.
    """
    with new_session() as session:
        query = select(TaskModel).filter_by(id=task_id)
        result = session.execute(query)
        task = result.scalars().first()
        if task is None:
            click.echo('task not found.')
            return
        click.echo(f'id={task.id}    description={task.description}    complete={task.complete}')


@hello.command()
@click.argument('description')
def create_task(description):
    """
    Create task with <DESCRIPTION>.
    """
    with new_session() as session:
        task_field = TaskModel(
            description=description,
            complete=False
        )
        session.add(task_field)
        session.flush()
        session.commit()
        click.echo(f'id={task_field.id}    description={task_field.description}    complete={task_field.complete}')


@hello.command()
@click.argument('task_id')
def change_complete(task_id):
    """
    Change task status to the opposite by <TASK_ID>.
    """
    with new_session() as session:
        query = select(TaskModel).filter_by(id=task_id)
        result = session.execute(query)
        task = result.scalars().first()
        if task is None:
            click.echo('task not found.')
            return
        task.complete = not task.complete
        session.flush()
        session.commit()
        click.echo(f'id={task.id}    description={task.description}    complete={task.complete}')


@hello.command()
@click.argument('task_id')
def delete_task(task_id):
    """
    Delete task by <TASK_ID>.
    """
    with new_session() as session:
        query = select(TaskModel).filter_by(id=task_id)
        result = session.execute(query)
        task = result.scalars().first()
        if task is None:
            click.echo('task not found.')
            return
        query = delete(TaskModel).filter_by(id=task_id)
        session.execute(query)
        session.flush()
        session.commit()
        click.echo(f'id={task.id}    description={task.description}    complete={task.complete}')

if __name__ == '__main__':
    hello()
