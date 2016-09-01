from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from .models import Invitation
from .forms import InvitationForm


# Creating new invitation from current user to another user
@login_required
def new_invitation(request):
    if request.method == 'POST':
        invitation = Invitation(from_user=request.user)  # Add sending user manually
        form = InvitationForm(data=request.POST, instance=invitation)  # Add other data
        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = InvitationForm()
    return render(request, "tictactoe/new_invitation.html", {'form': form})


# Accepting invitation
@login_required
def accept_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        # If user clicked 'accept' button
        if "accept" in request.POST:
            invitation.delete()  # Remove invitation from DB
            return HttpResponse("Invitation Accepted!")
        else:
            invitation.delete()
            return redirect('user_home')
    else:
        return render(request, "tictactoe/accept_invitation.html", {'invitation': invitation})
