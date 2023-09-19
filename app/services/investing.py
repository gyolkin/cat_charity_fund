from typing import List, TypeVar

from app.models import CharityProject, Donation

TargetType = TypeVar("TargetType", CharityProject, Donation)
SourceType = TypeVar("SourceType", CharityProject, Donation)


def investing_worker(
    target: TargetType, sources: List[SourceType]
) -> List[SourceType]:
    """
    Функция, выполняющая инвестирование неиспользованных средств в проекты.

    Описание: Пожертвование распределяется между проектами по принципу FIFO.
        Если проекты закрыты, то пожертвование используется в новом проекте.

    Ввод:
        target (Donation | CharityProject): Объект нового пожертвования
            или проекта.
        sources List[(Donation | CharityProject)]: Список открытых
            пожертвований или проектов.

    Вывод:
        List[(Donation | CharityProject)]: Список преобразованных пожертвований
            или проектов.
    """
    updated_sources = []
    for source in sources:
        source_to_close = source.full_amount - source.invested_amount
        target_to_close = target.full_amount - target.invested_amount
        distributable_amount = min(source_to_close, target_to_close)
        source.invested_amount += distributable_amount
        target.invested_amount += distributable_amount
        if source.invested_amount == source.full_amount:
            source.make_fully_invested()
        updated_sources.append(source)

    if target.invested_amount == target.full_amount:
        target.make_fully_invested()

    return updated_sources
