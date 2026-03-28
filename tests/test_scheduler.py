import sys
from pathlib import Path
import json

import pytest
from unittest.mock import MagicMock, mock_open

from scheduler import start_scheduler

# Ensure project root is on sys.path so 'scrapers' package can be imported in tests
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))



def test_start_scheduler(monkeypatch):
    
    fake_config={
        "jobs":[
            {"name":"kamera1"},
            {"name":"kamera2"}
        ]
    }
    m_open=mock_open(read_data=json.dumps(fake_config)) #mocking opening a fake file
    monkeypatch.setattr("builtins.open",m_open)

    target_modul=start_scheduler.__module__

    mock_scheduler_instance=MagicMock()
    mock_scheduler_class=MagicMock(return_value=mock_scheduler_instance)

    monkeypatch.setattr(f"{target_modul}.BlockingScheduler", mock_scheduler_class)
    monkeypatch.setattr(f"{target_modul}.WebCamScraper", mock_scheduler_class)

    start_scheduler()

    assert mock_scheduler_instance.add_job.call_count==2 # testing if scheduler made only 2 cases beceause for now there are only two of them
    
    cell_args_1=mock_scheduler_instance.add_job.call_args_list[0][1] #testing parameters of first job
    assert cell_args_1["id"]== "kamera1"
    assert cell_args_1["minutes"]==30

    cell_args_2=mock_scheduler_instance.add_job.call_args_list[1][1] # second job
    assert cell_args_2["id"]=="kamera2"

    mock_scheduler_instance.start.assert_called_once() # testing if it really starts


def test_start_schedular_empty(monkeypatch): #testting what happen in the file without task
    fake_config={"jobs":[]}

    m_open=mock_open(read_data=json.dumps(fake_config))
    monkeypatch.setattr("builtins.open",m_open)

    target_module=start_scheduler.__module__

    mock_scheduler_instance=MagicMock()
    mock_scheduler_class=MagicMock(return_value=mock_scheduler_instance)

    monkeypatch.setattr(f"{target_module}.BlockingScheduler", mock_scheduler_class)

    start_scheduler()

    mock_scheduler_instance.add_job.assert_not_called()

    mock_scheduler_instance.start.assert_called_once()


    
def test_start_schedular_file_not_found(monkeypatch):


    def mock_open_file_not_found(*args, **kwargs):
        raise FileNotFoundError("File not found")
    
    monkeypatch.setattr("builtins.open", mock_open_file_not_found)

    with pytest.raises(FileNotFoundError):
        start_scheduler()
