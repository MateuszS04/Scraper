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
    
    cell_args_1=mock_scheduler_instance.add_job.call_args_list[0][1]
    assert cell_args_1["id"]== "kamera1"
    assert cell_args_1["minutes"]==30
    
    

