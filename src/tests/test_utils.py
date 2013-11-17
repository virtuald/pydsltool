
from dsltool.utils import camelToSnake


def test_utils():
    '''From https://gist.github.com/jaytaylor/3660565'''
    
    assert camelToSnake('snakesOnAPlane') == 'snakes_on_a_plane'
    assert camelToSnake('SnakesOnAPlane') == 'snakes_on_a_plane'
    assert camelToSnake('snakes_on_a_plane') == 'snakes_on_a_plane'
    assert camelToSnake('IPhoneHysteria') == 'i_phone_hysteria'
    assert camelToSnake('iPhoneHysteria') == 'i_phone_hysteria'
    
